const STD = 1013;
const ISA = 15;

// True Airspeed
function calcTAS() {
    let ALT = parseFloat(document.getElementById("alt").value);
    let IAS = parseFloat(document.getElementById("ias").value);
    let QNH = parseFloat(document.getElementById("qnh").value);
    let OAT = parseFloat(document.getElementById("oat").value);

    let TH = ALT + ((STD - QNH) * 27);
    let K_ISA = ISA - 2 * (TH / 1000);
    let DH = TH + (120 * (OAT - K_ISA));

    let TAS = IAS * (1 + (DH / 1000) * 0.02);

    document.getElementById("tasResult").innerText = `TAS: ${TAS.toFixed(1)} kt`;
}

// WCA
function calcWCA() {
    let WS = parseFloat(document.getElementById("ws").value);
    let TAS = parseFloat(document.getElementById("tas2").value);
    let WD = parseFloat(document.getElementById("wd").value);
    let MT = parseFloat(document.getElementById("mt").value);

    let WA = (WD - MT + 360) % 360;
    let formula = (WS / TAS) * Math.sin(WA * Math.PI / 180);

    if (Math.abs(formula) > 1) {
        document.getElementById("wcaResult").innerText = "Fel: För stor vindkomponent.";
        return;
    }

    let WCA = Math.asin(formula) * 180 / Math.PI;
    let MH = (WCA + MT + 360) % 360;

    document.getElementById("wcaResult").innerText = `WCA: ${WCA.toFixed(1)}°`;
    document.getElementById("mhResult").innerText = `MH: ${MH.toFixed(1)}°`;
}

// Groundspeed
function calcGS() {
    let TAS = parseFloat(document.getElementById("tas3").value);
    let WS = parseFloat(document.getElementById("ws2").value);
    let WD = parseFloat(document.getElementById("wd2").value);
    let MH = parseFloat(document.getElementById("mh2").value);

    let WA = (WD - MH + 360) % 360;
    let GS = Math.sqrt(TAS*TAS + WS*WS - 2*TAS*WS*Math.cos(WA * Math.PI / 180));

    document.getElementById("gsResult").innerText = `GS: ${GS.toFixed(1)} kt`;
}

// Tryckhöjd
function calcTH() {
    let ALT = parseFloat(document.getElementById("alt2").value);
    let QNH = parseFloat(document.getElementById("qnh2").value);

    let TH = ALT + ((STD - QNH) * 27);

    document.getElementById("thResult").innerText = `TH: ${TH.toFixed(1)} ft`;
}

// Densitetshöjd
function calcDH() {
    let ALT = parseFloat(document.getElementById("alt3").value);
    let QNH = parseFloat(document.getElementById("qnh3").value);
    let OAT = parseFloat(document.getElementById("oat2").value);

    let TH = ALT + ((STD - QNH) * 27);
    let K_ISA = ISA - 2 * (TH / 1000);
    let DH = TH + (120 * (OAT - K_ISA));

    document.getElementById("dhResult").innerText = `DH: ${DH.toFixed(1)} ft`;
}

// Service worker
if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("sw.js");
}
