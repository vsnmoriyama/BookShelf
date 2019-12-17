 $(document).on('click', '#getIsbn', function () {
     var param1 = document.getElementsByName('isbn').item(0).value;
     var hostUrl = 'https://api.openbd.jp/v1/get?isbn=' + param1;
     $.getJSON(hostUrl, function (data) {
         if (data[0] == null) {
             alert("データが見つかりません");
         } else {
             document.getElementsByName('title').item(0).value = data[0].summary.title;
             document.getElementsByName('publisher').item(0).value = data[0].summary.publisher;
             document.getElementsByName('author').item(0).value = data[0].summary.author;
             function _lookup (obj, path) {
                 const keys = path.split('.');
                 for (let k in keys) {
                     const key = keys[k];
                     if (!obj.hasOwnProperty(key)) { return false; }
                     if (keys.length > 1) {
                         return _lookup(obj[key], keys.splice(1).join('.'));
                     }
                     return true;
                 }
             };
             if(_lookup(data[0], 'data[0].onix.DescriptiveDetail.Subject[0].SubjectCode')){
                 document.getElementsByName('genre').item(0).value = data[0].onix.DescriptiveDetail.Subject[0].SubjectCode;
             }
             if(_lookup(data[0], 'data[0].onix.CollateralDetail.TextContent[0].Text')){
                 document.getElementsByName('text').item(0).value = data[0].onix.CollateralDetail.TextContent[0].Text;
             }
             if(_lookup(data[0], 'data[0].onix.ProductSupply.SupplyDetail.Price[0].PriceAmount')){
                 document.getElementsByName('price').item(0).value = data[0].onix.ProductSupply.SupplyDetail.Price[0].PriceAmount;
             }
             var dateStr = data[0].summary.pubdate;
             var yyyy;
             var mm;
             var dd;
             if (dateStr.split('-').length == 3) {
                 splitDate = dateStr.split('-');
                 yyyy = splitDate[0];
                 mm = splitDate[1];
                 dd = splitDate[2];
             } else if (dateStr.split('-').length == 2) {
                 splitDate = dateStr.split('-');
                 yyyy = splitDate[0];
                 mm = splitDate[1];
                 dd = '01';
             } else if (dateStr.length > 6) {
                 yyyy = dateStr.substring(0, 4);
                 mm = dateStr.substring(4, 6);
                 dd = dateStr.substring(6, 8);
             } else if (dateStr.length > 4) {
                 yyyy = dateStr.substring(0, 4);
                 mm = dateStr.substring(4, 6);
                 dd = '01';
             } else {
                 yyyy = dateStr.substring(0, 4);
                 mm = '01';
                 dd = '01';
             }
             document.getElementsByName('pubdate').item(0).value = yyyy + '-' + mm + '-' + dd;
             document.getElementsByName('picture_name').item(0).value = data[0].summary.cover;
         }
     });
 });
 $(document).on('click', '#getRandom', function () {
     var hostUrl = 'http://localhost:8000/addBooks/getRandom';
     $.get(hostUrl);
 });