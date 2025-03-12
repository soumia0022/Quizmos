export class WordCloudGenerator {
    constructor(containerID, options = {}) {
        this.containerID = containerID;
        this.container = document.getElementById(containerID);
        
        // default
        this.config = {
            width: 600,
            height: 400,
            padding: 20,
            fontFamily: 'Arial, sans-serif',
            minFontSize: 12,
            maxFontSize: 60,
            fontSizeFunction: (count, maxCount) => {
                return Math.max(
                    this.config.minFontSize,
                    Math.sqrt(count / maxCount) * this.config.maxFontSize
                );
            },
            rotationAngles: [0], // no rotation
            spiralResolution: 0.5, // spread
            maxAttempts: 300,
            colorPalette: [
                '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
                '#9467bd', '#8c564b', '#e377c2', '#7f7f7f'
            ],
            // filter function that returns false for words containing "****"
            filterFunction: (text) => !text.includes('****')
        };

        // if there are any specified options put them with the default config
        this.config = { ...this.config, ...options };

        // create a SVG element
        this.svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
        this.svg.setAttribute('width', '100%');
        this.svg.setAttribute('height', '300');
        this.svg.setAttribute('viewBox', `0 0 ${this.config.width} ${this.config.height}`);
        this.container.innerHTML = '';
        this.container.appendChild(this.svg);


        this.placedWords = [];
    }

    // spiral placement path so all words are placed in a spiral order
    *spiralGenerator(centerX, centerY) {
        const angleStep = 0.1;
        const radiusStep = 5;
        let angle = 0;
        let radius = 0;

        while (true) {
            radius += radiusStep;
            angle += angleStep;

            const x = centerX + radius * Math.cos(angle);
            const y = centerY + radius * Math.sin(angle);

            yield { x, y };
        }
    }

    // checks for overlapping words
    isOverlapping(newWord) {
        return this.placedWords.some(placedWord => {
            const dx = Math.abs(newWord.x - placedWord.x);
            const dy = Math.abs(newWord.y - placedWord.y);

            const padding = 10;
            const combinedWidth = (newWord.width + placedWord.width) / 2 + padding;
            const combinedHeight = (newWord.height + placedWord.height) / 2 + padding;

            return dx < combinedWidth && dy < combinedHeight;
        });
    }

    // measures text size
    measureText(text, fontSize) {
        const svg = this.svg;
        const textElement = document.createElementNS("http://www.w3.org/2000/svg", "text");
        textElement.setAttribute('font-size', fontSize);
        textElement.setAttribute('font-family', this.config.fontFamily);
        textElement.textContent = text;


        svg.appendChild(textElement);//add to svg to get the size
        const bbox = textElement.getBBox();
        svg.removeChild(textElement);//remove it

        return {
            width: bbox.width,
            height: bbox.height
        };
    }


    generate(wordData) {
        // Clear previous words
        this.svg.innerHTML = '';
        this.placedWords = [];


        if (!wordData || Object.keys(wordData).length === 0) {
            const textElement = document.createElementNS("http://www.w3.org/2000/svg", "text");
            textElement.setAttribute('x', this.config.width / 2);
            textElement.setAttribute('y', this.config.height / 2);
            textElement.setAttribute('text-anchor', 'middle');
            textElement.setAttribute('fill', 'gray');
            textElement.textContent = 'No words submitted yet';
            this.svg.appendChild(textElement);
            return;
        }


        const maxCount = Math.max(...Object.values(wordData));

        // remove words containing "****" before creating the word cloud
        const filteredWordData = {};
        for (const [text, count] of Object.entries(wordData)) {
            if (this.config.filterFunction(text)) {
                filteredWordData[text] = count;
            }
        }


        if (Object.keys(filteredWordData).length === 0) {
            const textElement = document.createElementNS("http://www.w3.org/2000/svg", "text");
            textElement.setAttribute('x', this.config.width / 2);
            textElement.setAttribute('y', this.config.height / 2);
            textElement.setAttribute('text-anchor', 'middle');
            textElement.setAttribute('fill', 'gray');
            textElement.textContent = 'No appropriate words to display';
            this.svg.appendChild(textElement);
            return;
        }

        const words = Object.entries(filteredWordData)
            .map(([text, count]) => ({
                text,
                count,
                fontSize: this.config.fontSizeFunction(count, maxCount)
            }))
            .sort((a, b) => b.fontSize - a.fontSize);


        this.placeWords(words);
    }


    placeWords(words) {
        const centerX = this.config.width / 2;
        const centerY = this.config.height / 2;

        words.forEach(word => {
            const spiralGenerator = this.spiralGenerator(centerX, centerY);
            let placed = false;

            for (let attempts = 0; attempts < this.config.maxAttempts; attempts++) {
                const { x, y } = spiralGenerator.next().value;

                // Measure word dimensions
                const dims = this.measureText(word.text, word.fontSize);
                const testWord = {
                    x,
                    y,
                    width: dims.width,
                    height: dims.height,
                    text: word.text,
                    fontSize: word.fontSize
                };


                if (
                    x > this.config.padding &&
                    x < this.config.width - this.config.padding &&
                    y > this.config.padding &&
                    y < this.config.height - this.config.padding &&
                    !this.isOverlapping(testWord)
                ) {

                    const textElement = document.createElementNS("http://www.w3.org/2000/svg", "text");


                    const color = this.config.colorPalette[
                        Math.floor(Math.random() * this.config.colorPalette.length)
                    ];

                    textElement.setAttribute('x', x);
                    textElement.setAttribute('y', y);
                    textElement.setAttribute('font-size', word.fontSize);
                    textElement.setAttribute('fill', color);
                    textElement.setAttribute('font-family', this.config.fontFamily);
                    textElement.setAttribute('text-anchor', 'middle');
                    textElement.textContent = word.text;

                    this.svg.appendChild(textElement);


                    this.placedWords.push(testWord);
                    placed = true;
                    break;
                }
            }

        });
    }
}

