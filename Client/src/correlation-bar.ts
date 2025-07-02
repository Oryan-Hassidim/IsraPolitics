import { LitElement, TemplateResult, css, html, svg } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';
import { Task } from '@lit/task';

class Topic {
    constructor(public name: string, public value: number) {}
}

class MkPoint {
    constructor(
        public name: string,
        public image: string,
        public id: number,
        public topics: Topic[]
    ) {}
}

@customElement('correlation-bar')
export class CorrelationBar extends LitElement {
    @property({ type: String })
    topicA: string = '';

    @property({ type: String })
    topicB: string = '';

    private _points: MkPoint[] = [];

    private _mksTask = new Task(this, {
        task: async ([], { signal }) => {
            const response = await fetch('../client_data/mks.csv', { signal });
            if (!response.ok) throw new Error(response.statusText);
            const mkCsv = await response.text();
            const lines = mkCsv
                .split('\n')
                .slice(1)
                .map((line) => line.trim())
                .filter((line) => line)
                .map((line) => line.split(','));
            const urls = lines.map(
                (line) => `../client_data/mk_data/${line[0]}/main.json`
            );
            const fetchPromises = urls.map((url) =>
                fetch(url, { signal }).then((res) => {
                    if (!res.ok) throw new Error(res.statusText);
                    return res.json();
                })
            );
            const data = await Promise.all(fetchPromises);
        },
        args: () => [],
    });

    static styles = css`
        .container {
            display: grid;
            grid-template-columns: auto 1fr;
            grid-template-rows: 1fr auto;
        }
    `;

    override render(): TemplateResult<1> {
        return html`
            <div class="container">
                <div class="scale"></div>
                <div class="scale"></div>
            </div>
        `;
    }
}

declare global {
    interface HTMLElementTagNameMap {
        'correlation-bar': CorrelationBar;
    }
}
