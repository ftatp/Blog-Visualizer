function matching(user){
  chrome.tabs.executeScript({
    code : "document.querySelector('body').innerText"
  }, function(result){
      // 위의 코드가 실행된 후에 이 함수를 호출해주세요. 그 때 result에 담아주세요.
      // 이 문서에서 body 태그 아래에 있는 모든 텍스트를 가져온다.그 결과를 bodyText라는 변수에 담는다.
      var bodyText = result[0];
      // bodyText의 모든 단어를 추출하고, 그 단어의 숫자를 센다. 그 결과를 bodyNum이라는 변수에 담는다
      var bodyNum = bodyText.split(' ').length;
      // bodyText에서 자신이 알고 있는 단어(the,is)들이 몇번 등장하는지를 알아본다.그 결과를 myNum이라는 변수에 담는다.
      // G:전체
      // I: 대소문자 구분하지 않고
      var myNum = bodyText.match(new RegExp('\\b(' + user +')\\b','gi')).length;
      // per의 소숫점을 고정시킴
      var per = myNum/bodyNum*100;
      per = per.toFixed(1);
      // 내가 알고 있는 단어의 개수가 전체 중에 몇 %인지 알아보기
      // id값이 result인 태그에 결과를 추가한다.
      document.querySelector('#result').innerText = myNum + '/' + bodyNum + '\t(' + (per) + '%)';
  });
}




//크롬 스토리지에 저장된 값을 가져오세요.
chrome.storage.sync.get(function(data){
  //#user의 값으로 data를 입력해주세요.
  document.querySelector('#user').value = data.userWords;
  //분석해서 그 결과를 #result에 넣어주세요.
  matching(data.userWords);
});



//컨텐츠 페이즈의 #user 입력된 값이 변경 되었을 '때'
document.querySelector('#user').addEventListener('change', function(){
    //컨텐츠 페이지에 몇개의 단어가 등장하는지 계산해주세요.
    var user = document.querySelector('#user').value;
    // 크롬 스토리지에 입력값을 저장한다.
    chrome.storage.sync.set({
      userWords : user
    });
    //컨텐츠 페이지를 대상으로 코드를 실행해주세요.
    //크롬 확장의 기능 중에 tabs과 관련된 기능 중에 컨텐츠 페이지를 대상으로 아래와 같은 코드를 실행해주세요.
    //여기서 작성하기에는 너무 비좁음.
    matching(user);
});
