import { LitElement, TemplateResult, css, html, svg, unsafeCSS } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';
import { Lazy } from './Lazy';

export class SpeechPoint {
    constructor(
        public date: Date,
        public value: number,
        public tooltip: Lazy<TemplateResult | string> | null = null
    ) {}
}

class Point {
    constructor(public x: number, public y: number) {}
}

class PointString {
    constructor(public x: string, public y: string) {}
}

@customElement('mk-bar')
export class MkBar extends LitElement {
    //#region Properties
    @property({ type: Number })
    average: number = 0;

    @property({ type: Array })
    private _list: SpeechPoint[] = [];
    public get list(): SpeechPoint[] {
        return this._list;
    }
    public set list(value: SpeechPoint[]) {
        this._list = value.sort(this.compare_speeches_by_date);
        const min_date = this._list[0].date;
        const max_date = this._list[this._list.length - 1].date;
        const diff = max_date.getTime() - min_date.getTime();
        this._points_list = this._list.map((point) => {
            const x = (point.date.getTime() - min_date.getTime()) / diff;
            const y = point.value;
            return new Point(x, y);
        });
        this.requestUpdate();
    }
    //#endregion

    private _points_list: Point[] = [];

    @state()
    private _tooltip: TemplateResult | string | null = null;

    static animation_time = '0.5s';

    static styles = css`
        .my-bar-chart {
            --animation-time: ${unsafeCSS(MkBar.animation_time)};
            height: 30px;
            /* background-color: rgba(0, 0, 0, 0.1); */
            position: relative;
            transition: all var(--animation-time) ease-in-out;

            & .scale {
                position: absolute;
                top: 0%;
                left: 0%;
                width: 100%;
                height: 40%;
                --gradient-angle: 90deg;
                background: linear-gradient(
                    var(--gradient-angle),
                    red,
                    yellow,
                    green
                );
                border-radius: 10px;
                transition: all var(--animation-time) ease-in-out,
                    --gradient-angle var(--animation-time) ease-in-out;
            }
            & svg.chart {
                position: absolute;
                top: 20%;
                left: 0%;
                width: 100%;
                height: 80%;
                overflow: visible;
                transition: all var(--animation-time) ease-in-out;
                & .triangle-fill {
                    fill: black;
                    transition: opacity var(--animation-time) ease-in-out;
                }
                & circle {
                    fill: transparent;
                    transition: all var(--animation-time) ease-in-out;
                }
            }
            & .dates-axis {
                opacity: 0;
                position: absolute;
                bottom: 0%;
                left: 30px;
                right: 10px;
                height: 20%;
                transition: opacity var(--animation-time) ease-in-out;
                & ul {
                    justify-content: space-between;
                    width: 100%;
                    list-style-type: none;
                    padding: 0;
                    margin: 0;
                    /* position: relative; */
                    & li {
                        position: absolute;
                        bottom: 0%;
                        left: calc(var(--index) * 10%);
                        display: block;
                        transform-origin: 0px 50%;
                        transform: rotate(30deg);
                    }
                }
                & svg {
                    position: absolute;
                    top: 0%;
                    left: 0%;
                    width: 100%;
                    height: 30%;
                    & .axis {
                        stroke: black;
                        stroke-width: 2;
                        fill: none;
                    }
                    & .tick {
                        stroke: black;
                        stroke-width: 1;
                        fill: none;
                    }
                }
            }

            &:hover,
            &:focus-within {
                height: 100px;
                & .scale {
                    left: 10px;
                    width: 10px;
                    height: 60%;
                    --gradient-angle: 0deg;
                }
                & .dates-axis {
                    opacity: 1;
                }
                & svg.chart {
                    top: 0%;
                    left: 30px;
                    right: 10px;
                    width: calc(100% - 40px);
                    height: 60%;
                    & .triangle-fill {
                        opacity: 0;
                    }
                    & circle {
                        fill: red;
                        &:hover {
                            fill: blue;
                        }
                        title {
                            color: red;
                        }
                    }
                }
            }
            .tooltip {
                display: block;
                position: absolute;
                background-color: white;
                border: 1px solid black;
                padding: 5px;
                border-radius: 5px;
                font-size: 12px;
                pointer-events: visible;
                opacity: 0;
                transition: opacity var(--animation-time) ease-in-out,
                    left var(--animation-time) ease-in-out,
                    top var(--animation-time) ease-in-out;
            }
        }

        .tooltip:hover,
        .my-bar-chart:has(circle:hover) .tooltip,
        .my-bar-chart:has(circle:focus-within) .tooltip {
            opacity: 1;
        }
    `;

    private static getTime(date?: Date): number {
        return date != null ? date.getTime() : 0;
    }
    private compare_speeches_by_date(a: SpeechPoint, b: SpeechPoint) {
        return MkBar.getTime(a.date) - MkBar.getTime(b.date);
    }

    override render(): TemplateResult<1> {
        const avg_percent = (100.0 * this.average) / 5;
        const tri1_size = Math.floor(this._points_list.length / 3);
        const tri3_size = tri1_size;
        const tri2_size = Math.floor(
            this._points_list.length - 1 - tri1_size * 2
        );
        const triangle_points = Array.from(
            { length: tri1_size },
            (_, i) =>
                new PointString(
                    `calc(${avg_percent}% - ${(i * 7.0) / tri1_size}px)`,
                    `${(i * 100.0) / tri1_size}%`
                )
        )
            .concat(
                Array.from(
                    { length: tri2_size },
                    (_, i) =>
                        new PointString(
                            `calc(${avg_percent}% + ${
                                -7.0 + (i * 14.0) / tri2_size
                            }px)`,
                            `100%`
                        )
                )
            )
            .concat(
                Array.from(
                    { length: tri3_size },
                    (_, i) =>
                        new PointString(
                            `calc(${avg_percent}% + ${
                                7 - (i * 7.0) / tri3_size
                            }px)`,
                            `${100.0 - (i * 100.0) / tri3_size}%`
                        )
                )
            );
        triangle_points.push(triangle_points[0]); // close the triangle
        console.log(triangle_points);
        console.log(this._points_list);
        var lines = [];
        for (var i = 0; i < this._points_list.length - 1; i++) {
            lines.push(
                svg`
                    <line
                        x1="${triangle_points[i].x}"
                        y1="${triangle_points[i].y}"
                        x2="${triangle_points[i + 1].x}"
                        y2="${triangle_points[i + 1].y}"
                        stroke="black"
                        stroke-width="2"
                    >
                        <animate
                            dur="${MkBar.animation_time}"
                            fill="freeze"
                            begin="indefinite"
                            class="in"
                            attributeName="x1"
                            to="${this._points_list[i].x * 100.0}%"
                        ></animate>
                        <animate
                            dur="${MkBar.animation_time}"
                            fill="freeze"
                            begin="indefinite"
                            class="in"
                            attributeName="y1"
                            to="${100 - this._points_list[i].y * 100.0}%"
                        ></animate>
                        <animate
                            dur="${MkBar.animation_time}"
                            fill="freeze"
                            begin="indefinite"
                            class="in"
                            attributeName="x2"
                            to="${this._points_list[i + 1].x * 100.0}%"
                        ></animate>
                        <animate
                            dur="${MkBar.animation_time}"
                            fill="freeze"
                            begin="indefinite"
                            class="in"
                            attributeName="y2"
                            to="${100 - this._points_list[i + 1].y * 100.0}%"
                        ></animate>

                        <animate
                            dur="${MkBar.animation_time}"
                            fill="freeze"
                            begin="indefinite"
                            class="out"
                            attributeName="x1"
                            to="${triangle_points[i].x}"
                        ></animate>
                        <animate
                            dur="${MkBar.animation_time}"
                            fill="freeze"
                            begin="indefinite"
                            class="out"
                            attributeName="y1"
                            to="${triangle_points[i].y}"
                        ></animate>
                        <animate
                            dur="${MkBar.animation_time}"
                            fill="freeze"
                            begin="indefinite"
                            class="out"
                            attributeName="x2"
                            to="${triangle_points[i + 1].x}"
                        ></animate>
                        <animate
                            dur="${MkBar.animation_time}"
                            fill="freeze"
                            begin="indefinite"
                            class="out"
                            attributeName="y2"
                            to="${triangle_points[i + 1].y}"
                        ></animate>
                    </line>
                `
            );
        }
        // now add circles to the points
        const circles = this._points_list.map(
            (point, i) =>
                // when hover on a circle, tooltip is "x, y"
                svg`
                <circle @mouseenter=${this.show_tooltip}
                    @focusin=${this.show_tooltip}
                    cx="${point.x * 100.0}%"
                    cy="${100 - point.y * 100.0}%"
                    r="5px"
                    data-index="${i}"
                    tabindex="0"
                >
                </circle>`
        );

        const triangle_fill = svg`
            <polygon class="triangle-fill"
                points="0,1 -7,23 7,23"
                style="transform: translateX(calc(${avg_percent}%));"
                >
            </polygon>`;

        const dates_axis = this.calculate_dates_axis();

        return html`<div
            class="my-bar-chart"
            @mouseenter=${this.mouse_enter}
            @mouseleave=${this.mouse_leave}
            @focusin=${this.focus_in}
            @focusout=${this.focus_out}
            tabindex="0"
        >
            <div class="scale"></div>
            <svg class="chart">${triangle_fill} ${lines} ${circles}</svg>
            ${dates_axis}
            <div class="tooltip">${this._tooltip}</div>
        </div>`;
    }

    private calculate_dates_axis(): TemplateResult<1> {
        const min_date = this._list[0].date;
        const max_date = this._list[this._list.length - 1].date;
        const diff = max_date.getTime() - min_date.getTime();
        const dates = Array.from(
            { length: 11 },
            (_, i) =>
                html`<li style="--index: ${i}">
                    ${new Date(
                        min_date.getTime() + (diff * i) / 10
                    ).toLocaleDateString('he-IL', {
                        year: '2-digit',
                        month: '2-digit',
                        day: '2-digit',
                    })}
                </li>`
        );
        return html`<div class="dates-axis">
            <ul>
                ${dates}
            </ul>
            <svg>
                <line class="axis" x1="0%" y1="50%" x2="100%" y2="50%"></line>
                ${Array.from(
                    { length: 11 },
                    (_, i) =>
                        svg`
                        <line
                            class="tick"
                            x1="${i * 10}%"
                            y1="0%"
                            x2="${i * 10}%"
                            y2="100%"
                        ></line>
                    `
                )}
            </svg>
        </div>`; // TODO: implement the axis
    }

    private focus_within: boolean = false;

    // method for mouse enter
    private mouse_enter(e: MouseEvent): void {
        if (this.focus_within) return;
        this.shadowRoot?.querySelectorAll('.in').forEach((el) => {
            (el as SVGAnimateElement).beginElement();
        });
    }
    private mouse_leave(e: MouseEvent): void {
        if (this.focus_within) return;
        this.shadowRoot?.querySelectorAll('.out').forEach((el) => {
            (el as SVGAnimateElement).beginElement();
        });
    }
    private focus_in(e: FocusEvent): void {
        if (this.focus_within) return;
        this.focus_within = true;
        this.shadowRoot?.querySelectorAll('.in').forEach((el) => {
            (el as SVGAnimateElement).beginElement();
        });
    }
    private focus_out(e: FocusEvent) {
        if (e.relatedTarget) {
            const relatedTarget = e.relatedTarget as HTMLElement;
            if (
                relatedTarget.closest('.my-bar-chart') ===
                this.shadowRoot?.children[0]
            )
                return;
        }
        this.focus_within = false;
        this.shadowRoot?.querySelectorAll('.out').forEach((el) => {
            (el as SVGAnimateElement).beginElement();
        });
    }

    private async show_tooltip(e: MouseEvent) {
        const target = e.target as SVGCircleElement;
        const tooltip = this.shadowRoot?.querySelector(
            '.tooltip'
        ) as HTMLElement;
        const index = parseInt(target.getAttribute('data-index') || '0');
        const point = this.list[index];
        const formattedDate = point.date.toLocaleDateString('en-GB'); // Formats as DD/MM/YYYY
        this._tooltip = html`<div>${formattedDate}, ${point.value.toFixed(2)}</div>`;
        tooltip.style.left = `${target.cx.baseVal.value}px`;
        tooltip.style.top = `${target.cy.baseVal.value}px`;
        // now await for the tooltip of the point
        if (point.tooltip) {
            this._tooltip = await point.tooltip.get_value();
        }
    }
}

declare global {
    interface HTMLElementTagNameMap {
        'mk-bar': MkBar;
    }
}
