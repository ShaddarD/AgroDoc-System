// static/js/script.js

// Функция обновления данных заявителя
function updateZayavitelData() {
    const select = document.getElementById('zayavitel');
    const inn = document.getElementById('inn');
    const kpp = document.getElementById('kpp');
    const poPorucheniyu = document.getElementById('po_porucheniyu');
    
    if (select.value === 'bsg') {
        inn.value = '2315992271';
        kpp.value = '231501001';
        poPorucheniyu.value = 'ООО «АГРОИМПЭКС»';
    } else if (select.value === 'agro') {
        inn.value = '7816085379';
        kpp.value = '472501001';
        poPorucheniyu.value = '';
    } else if (select.value === 'new') {
        alert('Функция добавления нового заявителя будет доступна в следующей версии');
        select.value = 'bsg';
    }
    
    updatePreview();
}

// Расчет веса (тонны -> MT)
function calculateWeight() {
    const tons = parseFloat(document.getElementById('weight_tons').value) || 0;
    // Соотношение из ваших данных (664.9/133.14 ≈ 5)
    const mt = (tons / 5).toFixed(2);
    document.getElementById('weight_mt').value = mt;
    updatePreview();
}

// Расчет веса (MT -> тонны)
function calculateWeightReverse() {
    const mt = parseFloat(document.getElementById('weight_mt').value) || 0;
    const tons = (mt * 5).toFixed(1);
    document.getElementById('weight_tons').value = tons;
    updatePreview();
}

// Обновление превью данных
function updatePreview() {
    const preview = document.getElementById('previewData');
    
    const data = {
        'Заявитель': document.getElementById('zayavitel').options[document.getElementById('zayavitel').selectedIndex].text,
        'Продукт (рус)': document.getElementById('product_rus').value,
        'Продукт (eng)': document.getElementById('product_eng').value,
        'Вес, т': document.getElementById('weight_tons').value,
        'Вес, MT': document.getElementById('weight_mt').value,
        'Экспортер': document.getElementById('exp_rus').value,
        'Импортер': document.getElementById('imp_name').value,
        'Страна': document.getElementById('imp_country').value,
        'Место отбора': document.getElementById('inspection_place').value.substring(0, 30) + '...'
    };
    
    let html = '';
    for (let [key, value] of Object.entries(data)) {
        html += `
            <div class="data-item">
                <span class="data-label">${key}:</span>
                <span class="data-value">${value}</span>
            </div>
        `;
    }
    
    preview.innerHTML = html;
}

// Сохранение в "БД" (имитация)
function saveApplication() {
    alert('✅ Заявка сохранена в базу данных!\n\n(В реальной системе здесь будет обращение к серверу и запись в БД)');
    
    // Здесь будет AJAX запрос к Django API
    // collectFormData();
    // fetch('/api/applications/', {
    //     method: 'POST',
    //     headers: {
    //         'Content-Type': 'application/json',
    //         'X-CSRFToken': getCookie('csrftoken')
    //     },
    //     body: JSON.stringify(formData)
    // })
}

// Генерация документов
function generateDocuments() {
    alert('📄 Документы сформированы!\n\n(В реальной системе здесь происходит подстановка данных в шаблоны Word/Excel)');
    updatePreview();
}

// Просмотр документа
function previewDoc(docType) {
    let docName = '';
    switch(docType) {
        case 'cokz': docName = 'Заявка в ЦОК АПК'; break;
        case 'fito1': docName = 'Заявление на фитосертификат (лист 1)'; break;
        case 'fito2': docName = 'Заявление на отбор проб (лист 2)'; break;
        case 'act': docName = 'Акт досмотра'; break;
    }
    alert(`👁️ Просмотр документа: ${docName}\n\n(В реальной системе откроется предпросмотр PDF)`);
}

// Скачивание документа
function downloadDoc(docType) {
    let docName = '';
    switch(docType) {
        case 'cokz': docName = '04_качество_ЦОКЗ.docx'; break;
        case 'fito1': docName = 'ЗАЯВКИ_ФИТО_лист1.xlsx'; break;
        case 'fito2': docName = 'ЗАЯВКИ_ФИТО_лист2.xlsx'; break;
        case 'act': docName = 'Акт_ДОСМОТРА.xlsx'; break;
    }
    alert(`📥 Скачивание: ${docName}\n\n(В реальной системе файл будет сохранен на компьютер)`);
}

// Скачать все
function downloadAll() {
    alert('📦 Создание ZIP-архива со всеми документами...');
}

// Печать
function printAll() {
    alert('🖨️ Подготовка документов к печати...');
}

// Сбор данных формы (для отправки на сервер)
function collectFormData() {
    return {
        zayavitel: document.getElementById('zayavitel').value,
        po_porucheniyu: document.getElementById('po_porucheniyu').value,
        doverennost: document.getElementById('doverennost').value,
        exp_rus: document.getElementById('exp_rus').value,
        exp_eng: document.getElementById('exp_eng').value,
        exp_address: document.getElementById('exp_address').value,
        exp_inn: document.getElementById('exp_inn').value,
        exp_kpp: document.getElementById('exp_kpp').value,
        imp_name: document.getElementById('imp_name').value,
        imp_address: document.getElementById('imp_address').value,
        imp_country: document.getElementById('imp_country').value,
        imp_city: document.getElementById('imp_city').value,
        product_rus: document.getElementById('product_rus').value,
        product_eng: document.getElementById('product_eng').value,
        botanic_name: document.getElementById('botanic_name').value,
        weight_tons: document.getElementById('weight_tons').value,
        weight_mt: document.getElementById('weight_mt').value,
        packing: document.getElementById('packing').value,
        places: document.getElementById('places').value,
        containers: document.getElementById('containers').value,
        inspection_place: document.getElementById('inspection_place').value,
        doc_cokz: document.getElementById('doc_cokz').checked,
        doc_fito: document.getElementById('doc_fito').checked,
        doc_health: document.getElementById('doc_health').checked,
        doc_rad: document.getElementById('doc_rad').checked,
        permit: document.getElementById('permit').value
    };
}

// Получение CSRF токена для Django
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    updatePreview();
    
    // Добавляем обработчики для всех полей ввода
    const inputs = document.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.addEventListener('change', updatePreview);
        input.addEventListener('keyup', updatePreview);
    });
    
    // Добавляем обработчик для чекбокса фитосертификата
    const fitoCheckbox = document.getElementById('doc_fito');
    const permitBlock = document.getElementById('permit_block');
    
    if (fitoCheckbox && permitBlock) {
        fitoCheckbox.addEventListener('change', function() {
            permitBlock.style.display = this.checked ? 'block' : 'none';
        });
    }
});