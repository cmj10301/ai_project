// background → 웹 페이지로 메시지 전달
chrome.runtime.onMessage.addListener((request) => {
  if (request.type === "FROM_EXTENSION") {
    window.postMessage({
      type: "FROM_EXTENSION",
      payload: request.payload
    }, "*");
  }
});
