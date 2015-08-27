(function () {
  var tag = document.createElement('script');
  tag.src = "https://www.youtube.com/iframe_api";
  var firstScriptTag = document.getElementsByTagName('script')[0];
  firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
}());

var onYouTubeIframeAPIReady;
(function () {
  var apiKey;
  var player;
  var messageList = [];

  var onPlayerReady = function (event) {
    event.target.playVideo();
  };
  
  var onPlayerStateChange = function (event) {
    if (event.data === YT.PlayerState.PAUSED) {
      player.playVideo();
    }
  };

  onYouTubeIframeAPIReady = function () {
    player = new YT.Player('player', {
      height: '100%',
      width: '100%',
      videoId: '',
      events: {
        'onReady': onPlayerReady,
        'onStateChange': onPlayerStateChange
      }
    });
    setInterval(function () {
      if (player.getPlayerState() === YT.PlayerState.ENDED ||
          player.getPlayerState() === YT.PlayerState.UNSTARTED) {
        $.getJSON("/api/next", {
          apiKey: apiKey
        }, function (data) {
          if (data && data.length > 0) {
            player.loadVideoById(data);
          }
        });
      }
      $.getJSON("/api/state", {
        apiKey: apiKey
      }, function (data) {
        if (data.forceVideo) {
          player.loadVideoById(data.forceVideo);
        }
        if (data.messageList) {
          data.messageList.forEach(function (v) {
            var e = $("<div class=\"message\">"+v.sender+": "+v.body+"</div>");

            e.hide();
            $("#status").append(e);
            e.fadeIn(1500);

            setTimeout(function () {
              e.fadeOut(1500, function () {
                e.remove();
              });
            }, 5000);
          });
        }
        if (data.videoList) {
          $("#next").text("next -> "+data.videoList[0].name);
        } else {
          $("#next").text("empty playlist");
        }
      });
    }, 1500);
    apiKey = prompt("Please enter the API key.", "");
  };
}());

