let searchHistoryData = [];

chrome.storage.sync.get(['agreedToHistoryAccess'], (result) => {
  const agreed = result.agreedToHistoryAccess;
  updateUI(agreed);
});

document.getElementById("agreeBtn").addEventListener("click", () => {
  chrome.storage.sync.set({ agreedToHistoryAccess: true }, () => {
    updateUI(true);
  });
});

document.getElementById("fetchHistoryBtn").addEventListener("click", () => {
  const oneWeekAgo = Date.now() - 7 * 24 * 60 * 60 * 1000;
  chrome.history.search({ text: "", startTime: oneWeekAgo, maxResults: 100 }, (items) => {
    searchHistoryData = items;
    alert("검색 기록을 성공적으로 가져왔습니다!");
  });
});

document.getElementById("sendDataBtn").addEventListener("click", () => {
  if (!searchHistoryData.length) {
    alert("검색 기록을 먼저 가져와 주세요.");
    return;
  }

  // 현재 탭에 메시지 전달
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    chrome.tabs.sendMessage(tabs[0].id, {
      type: "FROM_EXTENSION",
      payload: searchHistoryData
    });
  });
});
  
function updateUI(agreed) {
  document.getElementById("statusText").textContent = agreed
    ? "✔ 검색 기록 수집에 동의하셨습니다."
    : "❗ 검색 기록 수집에 동의하지 않으셨습니다.";

  document.getElementById("fetchHistoryBtn").disabled = !agreed;
  document.getElementById("sendDataBtn").disabled = !agreed;
}
