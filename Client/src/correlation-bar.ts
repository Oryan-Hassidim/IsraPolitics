import { LitElement, TemplateResult, css, html, svg } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';
import { Task } from '@lit/task';
import { MkTooltip } from './mk-tooltip';
import { createRef, ref, Ref } from 'lit/directives/ref.js';

class Topic {
    constructor(public name: string, public value: number) {}
}

class MkData {
    constructor(public name: string, public image: string, public id: number) {}
}

class MkPoint extends MkData {
    topicA: number;
    topicB: number;

    constructor(
        id: number,
        name: string,
        image: string,
        topicA: number,
        topicB: number
    ) {
        super(name, image, id);
        this.topicA = topicA;
        this.topicB = topicB;
    }
}

@customElement('correlation-bar')
export class CorrelationBar extends LitElement {
    @property({ type: String })
    topicA: string = '';

    @property({ type: String })
    topicB: string = '';

    private _points: Map<number, MkPoint> = new Map();
    private _topics: Topic[] = [];
    private _mkData: Map<number, MkData> = new Map();

    private _mksTask = new Task(this, {
        task: async ([], { signal }) => {
            if (!this.topicA || !this.topicB) {
                throw new Error('Topics A and B must be set');
            }
            const mks_resp_task = fetch('../client_data/mks.csv', { signal });
            const topic1_resp_task = fetch(
                `../client_data/topics/${this.topicA}.json`,
                { signal }
            );
            const topic2_resp_task = fetch(
                `../client_data/topics/${this.topicB}.json`,
                { signal }
            );
            const [mks_resp, topic1_resp, topic2_resp] = await Promise.all([
                mks_resp_task,
                topic1_resp_task,
                topic2_resp_task,
            ]);
            if (!mks_resp.ok || !topic1_resp.ok || !topic2_resp.ok) {
                throw new Error('Failed to fetch data');
            }
            const mkCsv = await mks_resp.text();
            const mksLines = mkCsv
                .split('\n')
                .slice(1)
                .map((line) => line.trim())
                .filter((line) => line)
                .map((line) => line.split(','))
                .map((line) => {
                    return new MkData(
                        `${line[1]} ${line[2]}`,
                        line[4],
                        parseInt(line[0], 10)
                    );
                });
            this._mkData = new Map(mksLines.map((mk) => [mk.id, mk]));
            const topic1 = await topic1_resp.json();
            const topic2 = await topic2_resp.json();

            const mksId: number[] = Array.from(
                new Set(Object.keys(topic1).map(Number)).intersection(
                    new Set(Object.keys(topic2).map(Number))
                )
            );

            this._points = new Map(
                mksId.map((id) => {
                    return [
                        id,
                        new MkPoint(
                            id,
                            this._mkData.get(id)?.name || '',
                            this._mkData.get(id)?.image || '',
                            topic1[id],
                            topic2[id]
                        ),
                    ];
                })
            );
        },
        args: () => [],
    });

    static styles = css`
        :host {
            display: block;
            width: 100%;
            height: 100%;
        }
        .container {
            padding: 5em;
            display: grid;
            grid-template-columns: auto auto 1fr;
            grid-template-rows: 1fr auto auto;
            grid-template-areas:
                'label-y scale-y bar'
                'none none scale-x'
                'none none label-x';
        }
        .scale {
            border-radius: 0.5em;
        }
        .scale-x {
            grid-area: scale-x;
            height: 1em;
            width: 100%;
            background: linear-gradient(
                to right,
                red 0%,
                yellow 50%,
                green 100%
            );
        }
        .scale-y {
            grid-area: scale-y;
            width: 1em;
            height: 100%;
            background: linear-gradient(to top, red 0%, yellow 50%, green 100%);
        }
        .bar {
            grid-area: bar;
            width: 100%;
            height: 100%;
            position: relative;
        }
        .label {
            text-align: center;
        }
        .label-x {
            grid-area: label-x;
        }
        .label-y {
            writing-mode: sideways-lr;
            grid-area: label-y;
        }
        mk-tooltip {
            grid-area: bar;
        }
        #tooltip-anchor {
            grid-area: bar;
        }
    `;

    // function for generating the bar SVG
    private _generateBarSVG(): TemplateResult {
        return svg`
            ${this._points.values().map((point) => {
                return svg`<circle cx="${point.topicA * 10}"
                                   cy="${100 - point.topicB * 10}" 
                                   r="1" fill="black"
                                   data-id="${point.id}"
                                   @focusin="${this.point_focusin}"
                                   @mouseenter="${this.point_mouseenter}" />`;
            })}
        `;
    }

    override render() {
        // return html`hi`;
        return this._mksTask.render({
            pending: () => html`<div>Loading...</div>`,
            complete: () => html` <div class="container">
                <div class="scale scale-x"></div>
                <div class="scale scale-y"></div>
                <svg class="bar" viewBox="0 0 100 100">
                    ${this._generateBarSVG()}
                </svg>
                <span class="label label-x">נישואים אזרחיים</span>
                <span class="label label-y">התיישבות</span>
                <div id="tooltip-anchor" ${ref(this.tooltipAnchorRef)}></div>
                <mk-tooltip ${ref(this.tooltipRef)}></mk-tooltip>
            </div>`,
            error: (error) => html`<div>Error: ${error}</div>`,
        });
    }

    private tooltipRef: Ref<MkTooltip> = createRef();
    private tooltipAnchorRef: Ref<HTMLDivElement> = createRef();

    private point_focusin(e: FocusEvent) {
        const circle = e.target as SVGCircleElement;
        const idStr = circle.getAttribute('data-id');
        if (idStr === null) return;

        const id: number = parseInt(idStr, 10);
        const point = this._points.get(id);
        if (!point) return;
        if (!this.tooltipRef.value) return;

        this.tooltipRef.value.mkId = id;
        this.tooltipRef.value.name = point.name;
        this.tooltipRef.value.image = point.image;
    }
    private point_mouseenter(e: MouseEvent) {
        const circle = e.target as SVGCircleElement;
        const idStr = circle.getAttribute('data-id');
        if (idStr === null) return;

        const id: number = parseInt(idStr, 10);
        const point = this._points.get(id);
        if (!point) return;
        if (!this.tooltipRef.value) return;

        this.tooltipRef.value.mkId = id;
        this.tooltipRef.value.name = point.name;
        this.tooltipRef.value.image = point.image;
    }
}

declare global {
    interface HTMLElementTagNameMap {
        'correlation-bar': CorrelationBar;
    }
}
