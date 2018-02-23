(function () {
  'use strict';
  let video = document.querySelector('video')
    , canvas;
  const snapshotSound = document.getElementById('snapshot-sound');
  const $snapshotImg = $('img.snapshot');
  const $lookAlikeImg = $('img.look-alike');
  const $callToActionParagraph = $('.call-to-action');
  const $youLookLikeParagraph = $('.you-look-like');
  const $celebrityNameParagraph = $('.celebrity-name');

  /* particlesJS.load(@dom-id, @path-json, @callback (optional)); */
  particlesJS.load('body', 'style/particlesjs-config.json', function() {});

  /**
   *  Generates a still frame image from the stream in the <video>
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
    $lookAlikeImg.addClass('active');
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
      if (response && response.predictions && response.predictions.length) {
        let closestDistance = Infinity;
        let bestPrediction = response.predictions[0];
        for (let i = 0; i < response.predictions.length; i++) {
          const prediction = response.predictions[i];
          if (prediction.closest_image_distance < closestDistance) {
            closestDistance = prediction.closest_image_distance;
            bestPrediction = prediction;
          }
        }

        if (bestPrediction.closest_image) {
          $lookAlikeImg.attr('src', bestPrediction.closest_image);
          setTimeout(() => {
            $celebrityNameParagraph.text(bestPrediction.name).fadeIn();
            $youLookLikeParagraph.fadeIn();
          }, 1500)
        }
      }
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
