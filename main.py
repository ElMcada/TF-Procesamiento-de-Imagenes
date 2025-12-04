import tempfile
import os
import sys
from flask import Flask, request, redirect, send_file
from skimage import io
import base64
import glob
import numpy as np

app = Flask(__name__)

os.chdir(os.path.dirname(os.path.abspath(__file__)))

main_html = """
<!DOCTYPE html>
<html>
<head>
<title>Zona de Dibujo UPC</title>
<link href="https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap" rel="stylesheet">
<style>
    body {
        font-family: 'Fredoka One', cursive;
        background: linear-gradient(120deg, #84fab0 0%, #8fd3f4 100%);
        display: flex;
        flex-direction: column;
        align-items: center;
        min-height: 100vh;
        margin: 0;
        padding: 20px;
        color: #444;
    }

    h1 {
        color: #fff;
        text-shadow: 2px 2px 0px rgba(0,0,0,0.1);
        font-size: 2.5em;
        margin-bottom: 10px;
        text-align: center;
        background-color: rgba(0,0,0,0.1);
        padding: 10px 30px;
        border-radius: 50px;
    }

    .main-container {
        display: flex;
        gap: 40px;
        background: #fff;
        padding: 40px;
        border-radius: 40px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        align-items: center;
        justify-content: center;
        border: 5px solid #fff;
        flex-wrap: wrap;
    }

    .palette {
        display: flex;
        flex-direction: column;
        gap: 15px;
        padding: 15px;
        background: #f0f4f8;
        border-radius: 20px;
        border: 3px dashed #cbd5e0;
    }

    .color-btn {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        border: 4px solid #fff;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        cursor: pointer;
        transition: transform 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    .color-btn:hover { transform: scale(1.2); }

    .color-btn.active {
        transform: scale(1.1);
        border-color: #444;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.3);
    }

    .canvas-wrapper {
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    canvas {
        border: 10px solid #FFB84C;
        border-radius: 30px;
        cursor: crosshair;
        background-color: white;
        background-size: cover;
        box-shadow: 0 10px 0px #E5A544;
        touch-action: none;
    }

    .controls {
        display: flex;
        gap: 20px;
        width: 100%;
        justify-content: center;
        align-items: center;
        margin-top: 25px;
    }

    .btn {
        width: 160px;
        height: 50px;
        border: none;
        border-radius: 50px;
        font-family: 'Fredoka One', cursive;
        font-size: 18px;
        cursor: pointer;
        color: white;
        transition: all 0.1s;
        text-transform: uppercase;
        position: relative;
        top: 0;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .btn:active {
        top: 5px;
        box-shadow: 0 0 0 !important;
    }

    .btn-delete {
        background-color: #FF6B6B;
        box-shadow: 0 6px 0 #c94646;
    }
    .btn-delete:hover { background-color: #ff5252; }

    .btn-send {
        background-color: #4ECDC4;
        box-shadow: 0 6px 0 #3b9e96;
    }
    .btn-send:hover { background-color: #3bcbc2; }

    .logo {
        margin-bottom: 10px;
        filter: drop-shadow(0 4px 4px rgba(0,0,0,0.1));
    }
</style>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js" type="text/javascript"></script>
<script>
  var mousePressed = false;
  var lastX, lastY;
  var ctx;
  var canvas;
  var curColor = 'black';

   function getRndInteger(min, max) {
    return Math.floor(Math.random() * (max - min) ) + min;
   }

  function InitThis() {
      canvas = document.getElementById('myCanvas');
      ctx = canvas.getContext("2d");

      numero = getRndInteger(0, 10);
      letra = ["feliz", "triste", "sorprendido", "enojado", "neutral"];
      random = Math.floor(Math.random() * letra.length);
      aleatorio = letra[random];

      var emojiChar = "";
      if(aleatorio == "feliz") emojiChar = "😊";
      if(aleatorio == "triste") emojiChar = "😢";
      if(aleatorio == "sorprendido") emojiChar = "😲";
      if(aleatorio == "enojado") emojiChar = "😡";
      if(aleatorio == "neutral") emojiChar = "😐";

      document.getElementById('mensaje').innerHTML  = '¡Dibuja: <span style="color:#FF6B6B">' + aleatorio.toUpperCase() + ' ' + emojiChar + '</span>!';
      document.getElementById('numero').value = aleatorio;

      setGuideBackground(aleatorio);

      var firstBtn = document.querySelector('.color-btn');
      changeColor('black', firstBtn);

      function getMousePos(evt) {
        var rect = canvas.getBoundingClientRect();
        return {
          x: evt.clientX - rect.left,
          y: evt.clientY - rect.top
        };
      }

      $('#myCanvas').mousedown(function (e) {
          mousePressed = true;
          var pos = getMousePos(e);
          Draw(pos.x, pos.y, false);
      });

      $('#myCanvas').mousemove(function (e) {
          if (mousePressed) {
              var pos = getMousePos(e);
              Draw(pos.x, pos.y, true);
          }
      });

      $('#myCanvas').mouseup(function (e) {
          mousePressed = false;
      });
      $('#myCanvas').mouseleave(function (e) {
          mousePressed = false;
      });
  }

  function changeColor(color, btn) {
      curColor = color;
      var btns = document.getElementsByClassName('color-btn');
      for(var i=0; i<btns.length; i++) {
          btns[i].classList.remove('active');
          btns[i].style.borderColor = "#fff";
      }
      btn.classList.add('active');
  }

  function Draw(x, y, isDown) {
      if (isDown) {
          ctx.beginPath();
          ctx.strokeStyle = curColor;
          ctx.lineWidth = 15;
          ctx.lineCap = "round";
          ctx.lineJoin = "round";
          ctx.moveTo(lastX, lastY);
          ctx.lineTo(x, y);
          ctx.closePath();
          ctx.stroke();
      }
      lastX = x; lastY = y;
  }

  function clearArea() {
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
  }

  function prepareImg() {
     var canvas = document.getElementById('myCanvas');
     document.getElementById('myImage').value = canvas.toDataURL();
  }

  function setGuideBackground(emotion) {
      let svgContent = "";
      let colorGuia = "#555";
      let grosor = "8";

      // Coordenadas escaladas para 400x400
      let head = `<circle cx="200" cy="200" r="160" fill="none" stroke="${colorGuia}" stroke-width="${grosor}" stroke-dasharray="12,12" opacity="0.3" />`;
      let eyes = `<circle cx="140" cy="160" r="20" fill="none" stroke="${colorGuia}" stroke-width="${grosor}" stroke-dasharray="8,8" opacity="0.3" />
                  <circle cx="260" cy="160" r="20" fill="none" stroke="${colorGuia}" stroke-width="${grosor}" stroke-dasharray="8,8" opacity="0.3" />`;

      if (emotion === "feliz") {
          let mouth = `<path d="M 120 260 Q 200 340 280 260" fill="none" stroke="${colorGuia}" stroke-width="${grosor}" stroke-dasharray="12,12" opacity="0.3" />`;
          svgContent = head + eyes + mouth;
      } else if (emotion === "triste") {
          let mouth = `<path d="M 120 300 Q 200 220 280 300" fill="none" stroke="${colorGuia}" stroke-width="${grosor}" stroke-dasharray="12,12" opacity="0.3" />`;
          svgContent = head + eyes + mouth;
      } else if (emotion === "sorprendido") {
          let mouth = `<circle cx="200" cy="300" r="40" fill="none" stroke="${colorGuia}" stroke-width="${grosor}" stroke-dasharray="12,12" opacity="0.3" />`;
          svgContent = head + eyes + mouth;
      } else if (emotion === "enojado") {
          let mouth = `<line x1="120" y1="280" x2="280" y2="280" stroke="${colorGuia}" stroke-width="${grosor}" stroke-dasharray="12,12" opacity="0.3" />`;
          let brows = `<line x1="100" y1="120" x2="160" y2="140" stroke="${colorGuia}" stroke-width="${grosor}" stroke-dasharray="8,8" opacity="0.3" />
          <line x1="300" y1="120" x2="240" y2="140" stroke="${colorGuia}" stroke-width="${grosor}" stroke-dasharray="8,8" opacity="0.3" />`;
        svgContent = head + mouth + brows;
      } else if (emotion === "neutral") {
          let mouth = `<line x1="120" y1="280" x2="280" y2="280" stroke="${colorGuia}" stroke-width="${grosor}" stroke-dasharray="12,12" opacity="0.3" />`;
          svgContent = head + eyes + mouth;
      }

      let svgData = `<svg width="400" height="400" xmlns="http://www.w3.org/2000/svg">${svgContent}</svg>`;
      let url = "url('data:image/svg+xml;base64," + btoa(svgData) + "')";

      document.getElementById('myCanvas').style.backgroundImage = url;
  }
</script>
<body onload="InitThis();">

    <div class="logo">
      <img src="https://upload.wikimedia.org/wikipedia/commons/f/fc/UPC_logo_transparente.png" width="150"/>
    </div>

    <h1 id="mensaje">Cargando...</h1>

    <div class="main-container">
        <div class="palette">
            <div class="color-btn" style="background: #333;" onclick="changeColor('black', this)" title="Negro"></div>
            <div class="color-btn" style="background: #FF6B6B;" onclick="changeColor('#FF6B6B', this)" title="Rojo"></div>
            <div class="color-btn" style="background: #4ECDC4;" onclick="changeColor('#4ECDC4', this)" title="Turquesa"></div>
            <div class="color-btn" style="background: #45B7D1;" onclick="changeColor('#45B7D1', this)" title="Azul"></div>
            <div class="color-btn" style="background: #FFA502;" onclick="changeColor('#FFA502', this)" title="Naranja"></div>
        </div>

        <div class="canvas-wrapper">
            <canvas id="myCanvas" width="400" height="400"></canvas>

            <div class="controls">
                <button class="btn btn-delete" onclick="javascript:clearArea();return false;">Borrar</button>

                <form method="post" action="upload" onsubmit="javascript:prepareImg();" enctype="multipart/form-data" style="display:inline; margin:0;">
                    <input id="numero" name="numero" type="hidden" value="">
                    <input id="myImage" name="myImage" type="hidden" value="">
                    <button id="bt_upload" type="submit" class="btn btn-send">¡ENVIAR!</button>
                </form>
            </div>
        </div>
    </div>

</body>
</html>
"""


@app.route("/")
def main():
    return(main_html)

@app.route('/upload', methods=['POST'])
def upload():
    try:
        img_data = request.form.get('myImage').replace("data:image/png;base64,","")
        aleatorio = request.form.get('numero')

        print("Guardando imagen para:", aleatorio)

        if not os.path.exists(aleatorio):
            os.makedirs(aleatorio)

        with tempfile.NamedTemporaryFile(delete=False, mode="w+b", suffix='.png', dir=aleatorio) as fh:
            fh.write(base64.b64decode(img_data))

        print("Image uploaded successfully")
    except Exception as err:
        print("Error occurred:", err)

    return redirect("/", code=302)

@app.route('/prepare', methods=['GET'])
def prepare_dataset():
    images = []
    d = ["feliz", "triste", "sorprendido", "enojado", "neutral"]
    digits = []

    for digit in d:
        filelist = glob.glob('{}/*.png'.format(digit))

        if filelist:
            images_read = io.concatenate_images(io.imread_collection(filelist))

            if len(images_read.shape) == 4:
                images_read = images_read[:, :, :, 3]

            digits_read = np.array([digit] * images_read.shape[0])
            images.append(images_read)
            digits.append(digits_read)

    if images:
        images = np.vstack(images)
        digits = np.concatenate(digits)

        np.save('X.npy', images)
        np.save('y.npy', digits)
        return "¡OK! Archivos X.npy y y.npy generados correctamente."
    else:
        return "No se encontraron imágenes en las carpetas para procesar."

@app.route('/X.npy', methods=['GET'])
def download_X():
    if os.path.exists('./X.npy'):
        return send_file('./X.npy', as_attachment=True)
    else:
        return "Primero debes ir a /prepare para generar el archivo."

@app.route('/y.npy', methods=['GET'])
def download_y():
    if os.path.exists('./y.npy'):
        return send_file('./y.npy', as_attachment=True)
    else:
        return "Primero debes ir a /prepare para generar el archivo."

if __name__ == "__main__":
    digits = ["feliz", "triste", "sorprendido", "enojado", "neutral"]
    for d in digits:
        if not os.path.exists(d):
            os.makedirs(d)
