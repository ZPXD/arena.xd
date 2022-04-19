const serverPath = '/output/data';
const editorElem = document.querySelector(".code-editor");
const codeMirrorEditor = CodeMirror(editorElem, {
    value: "",
    mode: "python",
    lineNumbers: true,
    indentWithTabs: true,
    smartIndent: true,
    indentUnit: 4
});


const outputForm = document.querySelector('.output-field');
const buttonRun = document.querySelector(".run_btn");
const buttonClear = document.querySelector(".clean_btn");

buttonRun.addEventListener('click', () => {
    sendCodeToServerAndGetResults(codeMirrorEditor.getValue());
});

buttonClear.addEventListener('click', () => {
    outputForm.value = '';
});


function sendCodeToServerAndGetResults(data) {
    let dataToSend = {
        code: data
    };

    fetch(serverPath, {
        method: 'POST',
        headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
        body: JSON.stringify(dataToSend)
    }).then(response => response.json()).then(data => {
        console.log(data);
        if (data.status === 'ok') {
            outputForm.value = data.results;
        }
    }).catch((err) => {
        console.log('Błąd:' + err.message);
    });
}



function getCodeFromServer() {
    fetch(serverPath, {
        method: 'GET'
    }).then(response => response.text()).then(data => {
        console.log(data);
        codeMirrorEditor.setValue(data);

    }).catch(err => {
        console.log('Błąd:' + err.message);
    });
}

outputForm.value = '';
getCodeFromServer()
