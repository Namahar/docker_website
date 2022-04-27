const button = document.getElementById('go');
var callstack = [];
var tracker = 0;

if (button != null) {
    button.addEventListener('click', function() {
        $.ajax({
            url: 'backtrack',
            method: 'POST',
            success: function (response) {
                // response is json object of board
                // response[index (0, 1, 2, ...)] = board value

                // check if board is full
                var check = document.getElementById('1');

                if (check.innerHTML != '&nbsp;') {
                    clearBoard();
                }

                backtrack(response);
            }
        });
    });
}

function clearBoard() {
    for (let i = 0; i < 81; i++) {
        cell = document.getElementById((i+1).toString());
        cell.innerHTML = '&nbsp;';
    }

    return;
}

function updateBoard(board, init) {
    for (var cell in board) {
        
        // skip empty cells
        if (board[cell] == null) {
            continue;
        }

        tracker = cell;
        
        if (!init) {
            var prev = document.getElementById(tracker.toString());
            prev.style.removeProperty('color');
        }

        // get cell 
        var index = document.getElementById(cell.toString());

        if (index.innerHTML != board[cell] & !init) {
            index.style.cssText += 'color: yellow';
            index.innerHTML = board[cell];
        }
    }

    return;
}

function backtrack(board) {
    
    updateBoard(board, true);
    
    $.ajax({
        url: 'solve',
        method: 'POST',
        success: function (response) {
            // board is a json object of all games states during backtracking

            for (var state in response) {
                // get board state
                new_board = response[state];

                callstack.push(new_board);
            }

            runCallstack();
        }
    });

    return;    
}

function doUpdate(i) {
    setTimeout(function() {
        // console.log(i);
        updateBoard(callstack[i], false);
    }, 500*i);

    return;
}

function runCallstack() {

    // repeat final state for update
    lastIter = callstack[callstack.length - 1];
    callstack.push(lastIter);
    
    // console.log(callstack.length);


    for (var i = 0; i < callstack.length; i++) {
        doUpdate(i);
    }

    return;

}