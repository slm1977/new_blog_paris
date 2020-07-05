CKEDITOR.plugins.add( 'simpleImageUpload', {
    init: function( editor ) {
        var fileDialog = $('<input type="file">');
        
        fileDialog.on('change', function (e) {
            var uploadUrl = editor.config.uploadUrl;
            //var pageId = editor.config.pageId;
			var file = fileDialog[0].files[0];
			var imageData = new FormData();
            imageData.append('file', file);
            imageData.append('prefix', `page_${page_id}__`);

			$.ajax({
				url: uploadUrl,
				type: 'POST',
				contentType: false,
				processData: false,
				data: imageData,
			}).done(function(done) {
				var ele = editor.document.createElement('img');
				ele.setAttribute('src', done);
                editor.insertElement(ele);
                // prova a fare un refresh
                //  https://stackoverflow.com/questions/5663859/how-to-make-full-ckeditor-re-initialization
                console.log("Immagine caricata da plugin!!");
                // bug fixing: forzo per un attimo la visualizzazione
                // in modalita' sorgente per consentire il caricamento corretto
                // della immagine da parte del plugin image2
                editor.setMode('source');
                editor.setMode('wysiwyg');
			});

        })
        editor.ui.addButton( 'Image', {
            label: 'Carica una immagine',
            command: 'openDialog',
            toolbar: 'insert'
        });
        editor.addCommand('openDialog', {
            exec: function(editor) {
                fileDialog.click();
            }
        })
    }
});