var dt = new DataTransfer();

        $('.aside__input-file input[type=file]').on('change', function(){
        let $files_list = $(this).closest('.aside__input-file').next();
        $files_list.empty();
        
        for(var i = 0; i < this.files.length; i++){
        let new_file_input = '<div class="aside__input-file-list-item">' +
        '<div class="aside__input-file-list-item1">' +
        '<span class="aside__input-file-list-name">' + this.files.item(i).name + '</span>' + '</div>' +
        '<a href="#" onclick="removeFilesItem(this); return false;" class="aside__input-file-list-remove">x</a>' +
        '</div>';
        $files_list.append(new_file_input);
        dt.items.add(this.files.item(i));
        };
        this.files = dt.files;
        });
        
        function removeFilesItem(target){
        let name = $(target).prev().text();
        let input = $(target).closest('.aside__input-file-row').find('input[type=file]');
        $(target).closest('.aside__input-file-list-item').remove();
        for(let i = 0; i < dt.items.length; i++){
        if(name === dt.items[i].getAsFile().name){
        dt.items.remove(i);
        }
        }
        input[0].files = dt.files;
    }