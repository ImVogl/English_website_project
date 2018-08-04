        var modalWindow;
            modalWindow={
            _block: null,
            _win: null,
            //Метод инициализации блокирующего фона:
            initBlock: function() {
                _block = document.getElementById('blockscreen'); //Получаем наш блокирующий фон по ID
                
                //Если он не определен, то создадим его
                if (!_block) {
                    var parent = document.getElementsByTagName('body')[0]; //Получим первый элемент тега body
                    var obj = parent.firstChild; //Для того, чтобы вставить наш блокирующий фон в самое начало тега body
                    _block = document.createElement('div'); //Создаем элемент div
                    _block.id = 'blockscreen'; //Присваиваем ему наш ID
                    parent.insertBefore(_block, obj); //Вставляем в начало
                    _block.onclick = function() { //Добавим обработчик события по нажатию на                                                     блокирующий экран - закрыть модальное окно. 
                    modalWindow.close();
                    } 
                }
                _block.style.display = 'inline'; //Установим CSS-свойство        
            },
            //Метод инициализации диалогового окна:
            initWin: function(width, html, html_test) {
                _win = document.getElementById('modalwindow'); //Получаем наше диалоговое окно по ID
                //Если оно не определено, то также создадим его по аналогии
                if (!_win) {
                    var parent = document.getElementsByTagName('body')[0];
                    var obj = parent.firstChild;
                    _win = document.createElement('div');
                    _win.id = 'modalwindow';
                    _win.style.padding = '0 0 5px 0';
                    parent.insertBefore(_win, obj);
                }
                _win.innerHTML=html; //Добавим нужный HTML-текст в наше диалоговое окно
                _win.style.width = width + 'px'; //Установим ширину окна
                _win.style.display = 'inline'; //Зададим CSS-свойство
                //Установим позицию по центру экрана
                _win.style.left = '50%'; //Позиция по горизонтали
                _win.style.top = '50%'; //Позиция по вертикали
                //Выравнивание по центру путем задания отрицательных отступов
                _win.style.marginTop = -(_win.offsetHeight / 2) + 'px'; 
                _win.style.marginLeft = -(width / 2) + 'px';
                
                // настройка работы радиобатонов и чекбоксов
                var f = document.forms.Form; 
                f.onchange = function() { 
                    var n = f.querySelectorAll('[type="checkbox"]:checked'), 
                        l = f.querySelectorAll('[type="radio"]');
                    if (n.length>0) { 
                        l[3].disabled=true; 
                        l[3].checked=false; 
                    } else { 
                        l[3].disabled=false; 
                    } 
                }
                
                // реализация алгоритма отпракви формы на сервер, смены содержимого модального окна на форму теста, 
                // получения данных от сервера
                $( document ).ready(function() {
                    $("#sub_but").click(
		                function(){
			                sendAjaxForm('result_form', 'test_options', 'action_ajax_form.php');
			                html_change(html_test);
			                $("#btn").click(
                                function(){
                                    sendAjaxForm('result_form', 'test_form', 'action_ajax_form.php');
			                        return false;
                                }    
	                        );
		                }
		            );
                });
               
                // функция замены содержимого модального окна
                function html_change(html_ch) {
                    _win.innerHTML=html_ch;
                }
                
                // функция отправки форны на сервер и получения данных
                function sendAjaxForm(result_form, form_id, url) {
                    $.ajax({
                        url:     url, //url страницы (action_ajax_form.php)
                        type:     "POST", //метод отправки
                        dataType: "html", //формат данных
                        data: $("#"+form_id).serialize(),  // Сереарилизуем объект
                        success: function(response) { //Данные отправлены успешно
        	                result = $.parseJSON(response);
        	                $('#result_form').html('Имя: '+result.name);
    	                },
    	                error: function(response) { // Данные не отправлены
                            $('#result_form').html('Ошибка. Данные не отправлены.');
    	                }
    	            });
                }
            },
            
            //Метод закрытия модального окна:
            close: function() {
                document.getElementById('blockscreen').style.display = 'none';
                document.getElementById('modalwindow').style.display = 'none';        
            },
            
            //Метод появления модльного окна:
            show: function(width, html, html_test) {
                modalWindow.initBlock();
                modalWindow.initWin(width, html, html_test);
            }
        }