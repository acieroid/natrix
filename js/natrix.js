var context;
var sock;
var BLOCK_SIZE = 4;

function init() {
    context = $('#canvas')[0].getContext('2d');
    sock = new io.connect('http://' + window.location.hostname + ':8002', {
        rememberTransport: false
    });
    sock.on('board_size', board_size);
    sock.on('free', case_freed);
    sock.on('used', new_case);
    sock.on('food', new_food);
    sock.on('join', join);
    sock.on('died', died);
    $(document).keydown(handleKeyboard);

    $('#join').click(function () {
        if (valid_name($('#name').val())) {
            sock.emit('join', $('#name').val());
            log('Connecting');
        }
        else {
            log('Invalid name');
        }
    });

    $('#clear').click(function() { $('#log').text(''); });
};

function handleKeyboard(e) {
    switch (e.keyCode) {
    case 37:
        sock.emit('move', 'left');
        break;
    case 38:
        sock.emit('move', 'up');
        break;
    case 39:
        sock.emit('move', 'right');
        break;
    case 40:
        sock.emit('move', 'down');
        break;
    default:
        break;
    }
}

function valid_name(name) {
    return name != ''
}

function log(str) {
    $('#log').append(str + '<br/>')
    $('#log').scrollTop($('#log')[0].scrollHeight);
}

function fill_case(pos, color) {
    context.fillStyle = color;
    context.fillRect((pos[0]+1) * BLOCK_SIZE, (pos[1]+1) * BLOCK_SIZE,
                     BLOCK_SIZE, BLOCK_SIZE);
}

function draw_borders(width, height) {
    for (x = 0; x <= width+1; x++) {
        fill_case([x-1, -1], '#000');
        fill_case([x-1, height], '#000');
    }
    for (y = 0; y <= height+1; y++) {
        fill_case([-1, y-1], '#000');
        fill_case([width, y-1], '#000');
    }
}

function board_size(size) {
    $('#canvas')[0].width = (size[0]+2) * BLOCK_SIZE;
    $('#canvas')[0].height = (size[1]+2) * BLOCK_SIZE;
    draw_borders(size[0], size[1]);
}

function case_freed(pos) {
    fill_case(pos, '#fff');
}

function new_case(args) {
    pos = args[0];
    color = args[1];
    fill_case(pos, color);
}
    
function new_food(pos) {
    fill_case(pos, '#f00');
}

function join(args) {
    name = args[0];
    color = args[1];
    log('<span style="color: ' + color + '">' + name + '</span> joined the game');
}

function died(args) {
    name = args[0];
    color = args[1];
    log('<span style="color: ' + color + '">' + name + '</span> died');    
}
