
document.addEventListener('DOMContentLoaded', function() {
  const webSocketBridge = new channels.WebSocketBridge();
  const nl = document.querySelector("#notifylist");
  webSocketBridge.connect('/notifications/');  // todo: stop receiving every Case's notes
  webSocketBridge.listen(function(event) {
    console.log("RESPONSE:", event);
    if (event.case_id == "{{ case_id }}") {
      var el = document.createElement("span");
      el.innerHTML = `<br>    >>> ${event.case_last_log}`;
      nl.appendChild(el);
      var container = document.getElementById('notifylist');  // todo: detect scrollUp
      container.scrollTop = container.scrollHeight;
    }
  });
  document.ws = webSocketBridge; /* for debugging */
});