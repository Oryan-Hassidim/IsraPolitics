import { LitElement, TemplateResult, css, html, svg } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';
import { Task } from '@lit/task';
import { MkTooltip } from './mk-tooltip';
import { createRef, ref, Ref } from 'lit/directives/ref.js';

class Topic {
    constructor(public name: string) {}
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
    private _topics: Topic[] = [
        new Topic('התיישבות'),
        new Topic('נישואים_אזרחיים'),
    ];
    private _mkData: Map<number, MkData> = new Map();
    private _correlation: number = 0;

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
            this._correlation = this._calculateCorrelation();
        },
        args: () => [],
    });

    static styles = css`
        :host {
            display: grid;
            width: 100%;
            height: 100%;
            padding: 3em;
            box-sizing: border-box;
            place-content: stretch stretch;
            --animation-time: 0.4s;
        }

        input,
        input *,
        select,
        select * {
            font-family: inherit;
            font-size: inherit;
        }

        .container {
            display: grid;
            height: auto;
            margin: 0;
            grid-template-columns: auto auto 1fr;
            grid-template-rows: 1fr auto auto;
            grid-template-areas:
                'label-y scale-y bar'
                'none none scale-x'
                'none none label-x'
                'text text text';
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
        .point {
            position: absolute;
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background-color: black;
            transition: transform 0.1s ease-in-out;
            top: calc(attr(cy type(<number>)) * 1% - 3px);
            left: calc(attr(cx type(<number>)) * 1% - 3px);

            &:focus-within,
            &:hover {
                transform: scale(1.5) translateY(-1px);
                z-index: 1;
            }
        }
        .label {
            text-align: center;
            width: min-content;
            place-self: center;
            background: transparent;
            border-image-source: linear-gradient(
                to top right,
                #e6eeff 0%,
                #bfd3fe 100%
            );
            border-image-slice: 1;
            border-radius: 0.5em;
            border-width: medium;
        }
        .label-x {
            grid-area: label-x;
        }
        .label-y {
            writing-mode: sideways-lr;
            grid-area: label-y;
        }
        #tooltip-anchor {
            grid-area: bar;
            position: absolute;
            top: 0;
            left: 0;
            width: 2px;
            height: 2px;
            opacity: 1;
            background-color: transparent;
            transition: top var(--animation-time) ease,
                left var(--animation-time) ease;
            anchor-name: --tooltip-anchor;
            z-index: -1;
        }
        .tooltip {
            display: none;
            position: absolute;
            position-area: top;
            position-try-fallbacks: bottom;
            position-anchor: --tooltip-anchor;
            padding: 5px;
            pointer-events: visible;
            opacity: 0;
            transition: display var(--animation-time) ease allow-discrete,
                opacity var(--animation-time) ease,
                max-height var(--animation-time) ease,
                max-width var(--animation-time) ease;
            width: 200px;
            max-height: 0px;
            max-width: 0px;
            overflow: auto;
            font-size: 0.7em;
            z-index: 3;
            overflow-y: auto;
        }

        .tooltip:hover,
        .bar:has(.point:hover) .tooltip,
        .bar:has(.point:focus-within) .tooltip {
            display: grid;
            opacity: 1;
            max-height: 400px;
            max-width: 400px;
            overflow-x: hidden;
        }

        .text {
            grid-area: text;
            direction: rtl;
            h2 {
                text-align: center;
                font-weight: normal;
                margin-bottom: 0;
            }
        }
    `;

    // function for generating the bar SVG
    private _renderPoints(): TemplateResult {
        return html`
            ${Array.from(this._points.values())
                .sort((a, b) => a.topicA - b.topicA)
                .map((point) => {
                    return html`<div
                        class="point"
                        cx="${point.topicA * 10}"
                        cy="${100 - point.topicB * 10}"
                        data-id="${point.id}"
                        tabindex="0"
                        @focusin="${this._point_focusin}"
                        @mouseenter="${this._point_mouseenter}"
                    ></div>`;
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
                <div class="bar">
                    ${this._renderPoints()}
                    <div
                        id="tooltip-anchor"
                        ${ref(this.tooltipAnchorRef)}
                    ></div>
                    <mk-tooltip
                        class="tooltip"
                        ${ref(this.tooltipRef)}
                    ></mk-tooltip>
                </div>
                <!-- <span class="label label-x">${this.topicA}</span> -->
                <select
                    class="label label-x"
                    name="topicA"
                    title="Select Topic A"
                    @change="${this._onTopicAChange}"
                >
                    ${this._topics.map((topic) => {
                        return html`<option
                            value="${topic.name}"
                            ?selected="${topic.name === this.topicA}"
                        >
                            ${topic.name}
                        </option>`;
                    })}
                </select>
                <!-- <span class="label label-y">${this.topicB}</span> -->
                <select
                    class="label label-y"
                    name="topicB"
                    title="Select Topic B"
                    @change="${this._onTopicBChange}"
                >
                    ${this._topics.map((topic) => {
                        return html`<option
                            value="${topic.name}"
                            ?selected="${topic.name === this.topicB}"
                        >
                            ${topic.name}
                        </option>`;
                    })}
                </select>
                <div class="text">
                    <h2>
                        הקורלציה בין
                        <b>${this.topicA}</b>
                        ל<b>${this.topicB}</b>
                        היא
                        <b>${this._correlation.toFixed(2)}</b>
                    </h2>
                </div>
            </div>`,
            error: (error) => html`<div>Error: ${error}</div>`,
        });
    }

    private tooltipRef: Ref<MkTooltip> = createRef();
    private tooltipAnchorRef: Ref<HTMLDivElement> = createRef();

    private _onTopicAChange(e: Event) {
        const select = e.target as HTMLSelectElement;
        this.topicA = select.value;
        this._mksTask.run();
    }

    private _onTopicBChange(e: Event) {
        const select = e.target as HTMLSelectElement;
        this.topicB = select.value;
        this._mksTask.run();
    }

    private _point_focusin(e: FocusEvent) {
        const circle = e.target as HTMLDivElement;
        const idStr = circle.getAttribute('data-id');
        if (idStr === null) return;

        const id: number = parseInt(idStr, 10);
        const point = this._points.get(id);
        if (!point) return;
        if (!this.tooltipRef.value) return;

        this.tooltipRef.value.mkId = id;
        this.tooltipRef.value.name = point.name;
        this.tooltipRef.value.image = point.image;
        this.tooltipRef.value.innerHTML = `
            <span><b>${this.topicA}:</b> ${point.topicA.toFixed(2)}</span><br />
            <span><b>${this.topicB}:</b> ${point.topicB.toFixed(2)}</span>
        `;
        this.tooltipAnchorRef.value!.style.top = circle
            .computedStyleMap()
            .get('top')!
            .toString();
        this.tooltipAnchorRef.value!.style.left = circle
            .computedStyleMap()
            .get('left')!
            .toString();
    }

    private _point_mouseenter(e: MouseEvent) {
        const circle = e.target as HTMLDivElement;
        const idStr = circle.getAttribute('data-id');
        if (idStr === null) return;

        const id: number = parseInt(idStr, 10);
        const point = this._points.get(id);
        if (!point) return;
        if (!this.tooltipRef.value) return;

        this.tooltipRef.value.mkId = id;
        this.tooltipRef.value.name = point.name;
        this.tooltipRef.value.image = point.image;
        this.tooltipRef.value.innerHTML = `
            <span><b>${this.topicA}:</b> ${point.topicA.toFixed(2)}</span><br />
            <span><b>${this.topicB}:</b> ${point.topicB.toFixed(2)}</span>
        `;
        this.tooltipAnchorRef.value!.style.top = circle
            .computedStyleMap()
            .get('top')!
            .toString();
        this.tooltipAnchorRef.value!.style.left = circle
            .computedStyleMap()
            .get('left')!
            .toString();
    }

    private _calculateCorrelation(): number {
        const points = Array.from(this._points.values());
        if (points.length === 0) return 0;

        const n = points.length;
        // const sumX = points.reduce((sum, p) => sum + p.topicA, 0);
        // const sumY = points.reduce((sum, p) => sum + p.topicB, 0);
        // const sumXY = points.reduce((sum, p) => sum + p.topicA * p.topicB, 0);
        // const sumX2 = points.reduce((sum, p) => sum + p.topicA ** 2, 0);
        // const sumY2 = points.reduce((sum, p) => sum + p.topicB ** 2, 0);
        const [sumX, sumY, sumXY, sumX2, sumY2] = points.reduce(
            ([sumX, sumY, sumXY, sumX2, sumY2], p) => [
                sumX + p.topicA,
                sumY + p.topicB,
                sumXY + p.topicA * p.topicB,
                sumX2 + p.topicA ** 2,
                sumY2 + p.topicB ** 2,
            ],
            [0, 0, 0, 0, 0]
        );

        const numerator = n * sumXY - sumX * sumY;
        const denominator = Math.sqrt(
            (n * sumX2 - sumX ** 2) * (n * sumY2 - sumY ** 2)
        );

        return denominator === 0 ? 0 : numerator / denominator;
    }
}

declare global {
    interface HTMLElementTagNameMap {
        'correlation-bar': CorrelationBar;
    }
}
