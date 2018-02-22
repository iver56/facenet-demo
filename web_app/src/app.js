(function () {
  'use strict';
  let video = document.querySelector('video')
    , canvas;
  const snapshotSound = document.getElementById('snapshot-sound');
  const $snapshotImg = $('img.snapshot');
  const $lookAlikeImg = $('img.look-alike');
  const $callToActionParagraph = $('p.call-to-action');
  /**
   *  generates a still frame image from the stream in the <video>
   *  appends the image to the <body>
   */
  function takeSnapshot() {
    video.pause();
    const videoWidth = video.videoWidth;
    const videoHeight = video.videoHeight;
    const minVideoDim = Math.min(video.videoWidth, video.videoHeight);
    const xDiff = videoWidth - minVideoDim;
    const xOffset = xDiff / 2;
    const yDiff = videoHeight - minVideoDim;
    const yOffset = yDiff / 2;

    canvas = canvas || document.createElement('canvas');
    canvas.width = minVideoDim;
    canvas.height = minVideoDim;

    const ctx = canvas.getContext('2d');
    ctx.drawImage(
      video,  // drawable source
      xOffset,  // source offset x
      yOffset,  // source offset y
      minVideoDim,  // source width
      minVideoDim,  // source height
      0,  // destination offset x
      0,  // destination offset y
      minVideoDim,  // destination width
      minVideoDim  // destination height
    );

    const dataUrl = canvas.toDataURL('image/png');
    $snapshotImg.attr('src', dataUrl);
    $snapshotImg.addClass('active');
    snapshotSound.play();
    $callToActionParagraph.fadeOut(800);

    $(video).hide();
    const base64Png = dataUrl.replace('data:image/png;base64,', '');
    $.ajax({
      url: "/classify/",
      type: "POST",
      data: JSON.stringify({base64_png: base64Png}),
      dataType: "json",
      contentType: 'application/json'
    }).done(function(response) {
      $lookAlikeImg.addClass('active');
      if (response && response.predictions && response.predictions.length) {
        const prediction = response.predictions[0];
        if (prediction.image_references && prediction.image_references.length) {
          const imageReference = prediction.image_references[0];
          $lookAlikeImg.attr('src', `/celebrities/${imageReference[0]}/${imageReference[1]}`);
        }
      }
      //alert(response.predictions)
    }).fail(function(response) {
      alert('Server communication error');
      console.error(response);
    });
  }

  // Use the MediaDevices API
  // Docs: https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
  if (navigator.mediaDevices) {
    // Access the camera
    navigator.mediaDevices.getUserMedia({video: {facingMode: "user"}})
      .then(function (stream) {
        // permission granted
        video.srcObject = stream;

        document.addEventListener('keydown', (event) => {
          if (event.keyCode === 32) {
            event.preventDefault();
            takeSnapshot();
          }
        });
      })
      .catch(function (error) {
        // permission denied
        document.body.textContent = 'Could not access the camera. Error: ' + error.name;
      });
  }
})();
