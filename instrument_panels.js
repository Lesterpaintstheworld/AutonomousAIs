// Virtual Instrument Selection Panels

const instruments = {
    drums: ['Kick', 'Snare', 'Hi-hat', 'Tom', 'Crash', 'Ride'],
    synths: ['Lead', 'Pad', 'Bass', 'Arpeggiator', 'Pluck', 'FM'],
    bass: ['Electric', 'Synth', 'Upright', 'Slap', 'Fretless', 'Sub'],
    other: ['Piano', 'Guitar', 'Strings', 'Brass', 'Woodwinds', 'Percussion']
};

function createInstrumentPanel(category) {
    const panel = document.createElement('div');
    panel.className = 'instrument-panel';
    panel.innerHTML = `<h3>${category.charAt(0).toUpperCase() + category.slice(1)}</h3>`;

    const instrumentList = document.createElement('ul');
    instruments[category].forEach(instrument => {
        const listItem = document.createElement('li');
        listItem.innerHTML = `
            <button class="instrument-button" data-instrument="${instrument}">
                ${instrument}
            </button>
        `;
        instrumentList.appendChild(listItem);
    });

    panel.appendChild(instrumentList);
    return panel;
}

function initializeInstrumentPanels() {
    const container = document.getElementById('instrument-panels');
    Object.keys(instruments).forEach(category => {
        const panel = createInstrumentPanel(category);
        container.appendChild(panel);
    });

    // Event delegation for instrument selection
    container.addEventListener('click', (e) => {
        if (e.target.classList.contains('instrument-button')) {
            const selectedInstrument = e.target.dataset.instrument;
            console.log(`Selected instrument: ${selectedInstrument}`);
            // TODO: Implement logic to add the selected instrument to the sequencer
        }
    });
}

// Call this function when the page loads
document.addEventListener('DOMContentLoaded', initializeInstrumentPanels);
