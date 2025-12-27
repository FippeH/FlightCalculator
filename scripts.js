const STD = 1013;
const ISA = 15;

function $(id) { return document.getElementById(id); }

function createInput(id, label) {
    return `
        <label>${label}</label>
        <input id="${id}" type="number">
    `;
}

function createText(id, label) {
    return `
        <label>${label}</label>
        <input id="${id}" type="text">
    `;
}

function showForm(html, callback) {
    $("formContainer").innerHTML = html + `<button id="calcBtn">Beräkna</button>`;
    $("calcBtn").onclick = callback;
}

function result(text) {
    $("result").innerHTML = `<b>${text}</b>`;
}

$("toolSelect").onchange = function () {
    const tool = this.value;
    $("result").innerHTML = "";

    if (tool === "tas") {
        showForm(
            createInput("alt", "Höjd (fot)") +
            createInput("ias", "IAS (knop)") +
            createInput("qnh", "QNH") +
            createInput("oat", "Temperatur (°C)"),
            () => {
                let ALT = +$("alt").value;
                let IAS = +$("ias").value;
                let QNH = +$("qnh").value;
                let OAT = +$("oat").value;

                let TH = ALT + ((STD - QNH) * 27);
                let K_ISA = ISA + (-2 * (TH / 1000));
                let DH = TH + (120 * (OAT - K_ISA));
                let TAS = IAS * (1 + (DH / 1000) * 0.02);

                result(`True Airspeed: ${TAS.toFixed(1)} kt`);
            }
        );
    }

    if (tool === "wca") {
        showForm(
            createInput("ws", "Vindhastighet (knop)") +
            createInput("tas", "TAS (knop)") +
            createInput("wd", "Vindriktning") +
            createInput("mt", "Magnetisk track"),
            () => {
                let WS = +$("ws").value;
                let TAS = +$("tas").value;
                let WD = +$("wd").value;
                let MT = +$("mt").value;

                let WA = (WD - MT + 360) % 360;
                let Formel = (WS / TAS) * Math.sin(WA * Math.PI / 180);

                if (Math.abs(Formel) > 1) {
                    result("Fel: Vindkomponenten är för stor.");
                    return;
                }

                let WCA = Math.asin(Formel) * 180 / Math.PI;
                let MH = (WCA + MT + 360) % 360;

                result(`WCA: ${WCA.toFixed(1)}°<br>Magnetisk kurs: ${MH.toFixed(1)}°`);
            }
        );
    }

    if (tool === "gs") {
        showForm(
            createInput("tas", "TAS (knop)") +
            createInput("ws", "Vindhastighet (knop)") +
            createInput("wd", "Vindriktning") +
            createInput("mh", "Magnetisk kurs"),
            () => {
                let TAS = +$("tas").value;
                let WS = +$("ws").value;
                let WD = +$("wd").value;
                let MH = +$("mh").value;

                let WA = (WD - MH + 360) % 360;
                let GS = Math.sqrt(TAS*TAS + WS*WS - 2*TAS*WS*Math.cos(WA*Math.PI/180));

                result(`Markhastighet: ${GS.toFixed(1)} kt`);
            }
        );
    }

    if (tool === "th") {
        showForm(
            createInput("alt", "Höjd (fot)") +
            createInput("qnh", "QNH"),
            () => {
                let ALT = +$("alt").value;
                let QNH = +$("qnh").value;

                let TH = ALT + ((STD - QNH) * 27);
                result(`Tryckhöjd: ${TH.toFixed(1)} ft`);
            }
        );
    }

    if (tool === "dh") {
        showForm(
            createInput("alt", "Höjd (fot)") +
            createInput("qnh", "QNH") +
            createInput("oat", "Temperatur (°C)"),
            () => {
                let ALT = +$("alt").value;
                let QNH = +$("qnh").value;
                let OAT = +$("oat").value;

                let TH = ALT + ((STD - QNH) * 27);
                let K_ISA = ISA + (-2 * (TH / 1000));
                let DH = TH + (120 * (OAT - K_ISA));

                result(`Densitetshöjd: ${DH.toFixed(1)} ft`);
            }
        );
    }

    if (tool === "vk") {
        showForm(
            createInput("rw", "Bana") +
            createInput("wd", "Vindriktning") +
            createInput("ws", "Vindhastighet (knop)"),
            () => {
                let RW = +$("rw").value;
                let WD = +$("wd").value;
                let WS = +$("ws").value;

                let WA = (WD - RW + 360) % 360;
                let rad = WA * Math.PI / 180;

                let SV = Math.sin(rad) * WS;
                let MV = Math.cos(rad) * WS;

                result(`
                    Sidvind: ${Math.abs(SV).toFixed(1)} kt<br>
                    Mot-/medvind: ${Math.abs(MV).toFixed(1)} kt
                `);
            }
        );
    }

    if (tool === "rr") {
        showForm(
            createInput("alt", "Flygplanets höjd (fot)") +
            createInput("gnd", "Stationens höjd (fot)"),
            () => {
                let ALT = +$("alt").value;
                let GND = +$("gnd").value;

                let RR = 1.225 * (Math.sqrt(ALT) + Math.sqrt(GND));
                result(`Radioräckvidd: ${RR.toFixed(1)} NM`);
            }
        );
    }

    if (tool === "bt") {
        showForm(
            createText("on", "ON-BLOCK (HHMM)") +
            createText("off", "OFF-BLOCK (HHMM)"),
            () => {
                let on = $("on").value;
                let off = $("off").value;

                let ON = parseInt(on.slice(0,2))*60 + parseInt(on.slice(2));
                let OFF = parseInt(off.slice(0,2))*60 + parseInt(off.slice(2));

                if (OFF < ON) OFF += 1440;

                let diff = OFF - ON;
                result(`Blocktid: ${(diff/60).toFixed(1)} h (${diff} min)`);
            }
        );
    }

    if (tool === "metar") {
        showForm(
            createText("icao", "ICAO-kod"),
            async () => {
                let ICAO = $("icao").value.toUpperCase();

                let metUrl = `https://aro.lfv.se/Links/Link/ViewLink?TorLinkId=314&type=MET&icao=${ICAO}`;
                let tafUrl = `https://aro.lfv.se/Links/Link/ViewLink?TorLinkId=315&type=MET&icao=${ICAO}`;

                let met = await fetch(metUrl).then(r => r.text());
                let taf = await fetch(tafUrl).then(r => r.text());

                result(`<pre>${met}\n\n${taf}</pre>`);
            }
        );
    }
};
