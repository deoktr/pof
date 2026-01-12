// disable obfuscate button on query
const button = document.getElementById("obfuscateButton");
document.body.addEventListener('htmx:configRequest', function() {
    button.disabled = true;
});
document.body.addEventListener('htmx:afterOnLoad', function() {
    button.disabled = false;
});
document.body.addEventListener('htmx:responseError', function() {
    button.disabled = false;
});

// copy the output to clipboard
document.getElementById("copyButton").onclick = function() {
    const content = document.getElementById("output").innerText.trimEnd();
    navigator.clipboard.writeText(content).catch(err => {
        console.error("Failed to copy: ", err);
    });
};
