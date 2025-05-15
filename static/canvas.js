window.addEventListener('DOMContentLoaded', () => {
  const canvas = new fabric.Canvas('noboriCanvas', {
    backgroundColor: '#fff',
    preserveObjectStacking: true
  });

  // テキスト追加（修正：textInputの値を使用）
  document.getElementById('addTextButton').onclick = () => {
    const input = document.getElementById('textInput').value.trim();
    const text = new fabric.Textbox(input || 'テキスト', {
      left: 100,
      top: 100,
      fontSize: 32,
      fill: '#000',
      fontFamily: document.getElementById('fontSelect').value || 'Arial',
    });
    canvas.add(text).setActiveObject(text);
  };

  // 四角追加
  document.getElementById('addRectButton').onclick = () => {
    const rect = new fabric.Rect({
      left: 150,
      top: 150,
      width: 100,
      height: 100,
      fill: '#00BFFF'
    });
    canvas.add(rect).setActiveObject(rect);
  };

  // 円追加
  document.getElementById('addCircleButton').onclick = () => {
    const circle = new fabric.Circle({
      left: 200,
      top: 200,
      radius: 50,
      fill: '#FF69B4'
    });
    canvas.add(circle).setActiveObject(circle);
  };

  // 色変更（修正：未選択時に警告）
  document.getElementById('colorPicker').onchange = (e) => {
    const obj = canvas.getActiveObject();
    if (obj) {
      obj.set('fill', e.target.value);
      canvas.requestRenderAll();
    } else {
      alert("オブジェクトを選択してください。");
    }
  };

  // フォント変更
  document.getElementById('fontSelect').onchange = (e) => {
    const obj = canvas.getActiveObject();
    if (obj && obj.type === 'textbox') {
      obj.set('fontFamily', e.target.value);
      canvas.requestRenderAll();
    }
  };

  // 縦書き切り替え
  document.getElementById('toggleVertical').onclick = () => {
    const obj = canvas.getActiveObject();
    if (obj && obj.type === 'textbox') {
      const original = obj.text.replace(/\n/g, '');
      const isVertical = !obj.text.includes('\n');
      obj.set('text', isVertical ? original.split('').join('\n') : original);
      canvas.requestRenderAll();
    }
  };

  // 画像アップロード
  document.getElementById('uploadImage').addEventListener('change', (e) => {
    const reader = new FileReader();
    reader.onload = function (event) {
      fabric.Image.fromURL(event.target.result, function (img) {
        img.scaleToWidth(200);
        img.set({ left: 100, top: 100 });
        canvas.add(img).setActiveObject(img);
      });
    };
    reader.readAsDataURL(e.target.files[0]);
  });

  // 削除
  document.getElementById('deleteButton').onclick = () => {
    const active = canvas.getActiveObject();
    if (active) {
      canvas.remove(active);
    }
  };

  // 保存（PNG）
  document.getElementById('saveButton').onclick = () => {
    const dataURL = canvas.toDataURL({ format: 'png' });
    const link = document.createElement('a');
    link.download = 'nobori_design.png';
    link.href = dataURL;
    link.click();
  };


  // 🔽 ここに追加：前面へ
  document.getElementById('bringToFront').addEventListener('click', () => {
    const activeObject = canvas.getActiveObject();
    if (activeObject) {
      canvas.bringToFront(activeObject);
      canvas.requestRenderAll();
    }
  });

  // 🔽 ここに追加：背面へ
  document.getElementById('sendToBack').addEventListener('click', () => {
    const activeObject = canvas.getActiveObject();
    if (activeObject) {
      canvas.sendToBack(activeObject);
      canvas.requestRenderAll();
    }
  });
});