 function notification(){
   var img = whale.runtime.getURL('resource/project/icon_good.png')
   $.notify({
     position:'top-right',
     icon:img,
     className: 'el-notification',
     timeout: 2000,
     closeIcon: '',
     closable: true, // is closable?
     offset: 16 // in pixels
   });

   $('.el-notification').css('width','auto');
   $('.el-notification').css('background-color','');
   $(".el-notification").delay(600).fadeTo("slow", 0.2);
   $('.el-notification').click(function(){
      whale.runtime.sendMessage({msg: 'sidebar on'});
     });
 };

notification();
