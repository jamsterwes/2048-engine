var boards = [];
var moves = [];
var cells = {
        0: "rgba(238, 228, 218, 0.35)",
        2: "rgb(238, 228, 218)",
        4: "rgb(237, 224, 200)",
        8: "rgb(242, 177, 121)",
        16: "rgb(245, 149, 99)",
        32: "rgb(246, 124, 95)",
        64: "rgb(246, 94, 59)",
        128: "rgb(237, 207, 114)",
        256: "rgb(237, 204, 97)",
        512: "rgb(237, 200, 80)",
        1024: "rgb(237, 197, 63)"
}
var back = "rgb(178, 170, 162)";
var margin = 10;
var dim = 80;

eel.expose(initBoards);
function initBoards(amt) {
    for (var i = 0; i < amt; i++) {
        moves.push(0);
        boards.push([]);
        var cont = document.createElement("div");
        cont.id = "cont" + i.toString();
        cont.className = "cont";
        var title = document.createElement('h3');
        title.id = "title" + i.toString();
        var sub = document.createElement('h4');
        sub.id = "sub" + i.toString();
        sub.className = "sub";
        var canvas = document.createElement('canvas');
        canvas.width = dim * 4;
        canvas.height = dim * 4;
        canvas.id = "board" + i.toString();
        cont.appendChild(title);
        cont.appendChild(sub);
        cont.appendChild(canvas);
        document.body.appendChild(cont);
    }
}

eel.expose(update);
function update(boardId, moveI, boardMat, sub) {
    console.log(JSON.parse(boardMat));
    boardMat = JSON.parse(boardMat);
    boards[boardId] = boardMat;
    moves[boardId] = moveI
    setTitle(boardId, "Board #" + (boardId + 1).toString() + " - Move #" + moves[0].toString(), sub);
    drawBoard(boardId);
}

function setTitle(boardId, title, sub) {
    document.getElementById("title" + boardId.toString()).innerText = title;
    document.getElementById("sub" + boardId.toString()).innerText = sub;
}

function drawBoard(boardId, boardMat) {
    var cv = document.getElementById("board" + boardId);
    var ctx = cv.getContext('2d');
    ctx.fillStyle = back;
    ctx.fillRect(0, 0, dim * 4, dim * 4);
    for (var y = 0; y < 4; y++) {
        for (var x = 0; x < 4; x++) {
            var val = boards[boardId][y][x];
            ctx.fillStyle = cells[val];
            ctx.fillRect(x*dim + margin, y*dim + margin, dim - margin * 2, dim - margin * 2);
            if (val > 4) {
                ctx.fillStyle = "rgb(255, 255, 255)";
            } else {
                ctx.fillStyle = "rgb(119, 110, 101)";
            }
            if (val > 0) {
                ctx.font = "24px 'Arial'"
                ctx.textAlign = "center";
                ctx.textBaseline = "middle";
                ctx.fillText(val.toString(), x*dim + (dim / 2), y*dim + (dim / 2), dim);
            }
        }
    }
}

eel.onload();
