 $(document).on('click', '#getIsbn', function () {
   var param1 = document.getElementsByName('isbn').item(0).value;
   var hostUrl = 'https://api.openbd.jp/v1/get?isbn=' + param1;
   $.getJSON(hostUrl, function (data) {
     if (data[0] == null) {
       alert("データが見つかりません");
     } else {
       if (data[0].summary.cover == "") {
         $("#thumbnail").html('<img src=\"\" />');
       } else {
         $("#thumbnail").html('<img src=\"' + data[0].summary.cover + '\" style=\"border:solid 1px #000000\" />');
       }
       document.getElementsByName('title').item(0).value = data[0].summary.title;
       document.getElementsByName('publisher').item(0).value = data[0].summary.publisher;
       document.getElementsByName('author').item(0).value = data[0].summary.author;
       var dateStr = data[0].summary.pubdate;
       var yyyy = dateStr.substring(0,4);
       var mm = dateStr.substring(4,6);
       var dd = dateStr.substring(6,8);
       document.getElementsByName('pubdate').item(0).value = yyyy + '-' + mm + '-' + dd;
       document.getElementsByName('picture_name').item(0).value = data[0].summary.cover;
     }
   });
 });
  $(document).on('click', '#getRandom', function () {
   var hostUrl = 'http://localhost:8000/addBooks/getRandom';
   $.get(hostUrl);
 });