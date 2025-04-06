import { LitElement, TemplateResult, css, html, svg, unsafeCSS } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';
import { Lazy } from './helpers/Lazy';
import { createRef, Ref, ref } from 'lit/directives/ref.js';
import { DatesHelpers, DateType } from './helpers/DatesHelpers';

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
    @property({ type: Number })
    average: number = 0;

    private _list: SpeechPoint[] = [];
    public get list(): SpeechPoint[] {
        return this._list;
    }
    @property({ type: Array })
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

    private _points_list: Point[] = [];

    @state()
    private _tooltip_content: TemplateResult | string | null = null;

    static animation_time_in_s = 0.5;

    static styles = css`
        .my-bar-chart {
            --animation-time: ${MkBar.animation_time_in_s}s;
            height: 30px;
            /* background-color: rgba(0, 0, 0, 0.1); */
            position: relative;
            transition: all var(--animation-time) ease-in-out;

            .scale {
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
            svg.chart {
                position: absolute;
                top: 30%;
                left: 0%;
                width: 100%;
                height: 80%;
                overflow: visible;
                transition: all var(--animation-time) ease-in-out;
                line {
                    stroke: black;
                    stroke-width: 6px;
                    transition: stroke-width var(--animation-time);
                    transition-delay: calc(
                        var(--date-ratio) * var(--animation-time)
                    );
                    stroke-linecap: round;
                }
                .triangle-fill {
                    fill: black;
                    opacity: 1;
                    transition: opacity var(--animation-time),
                        fill var(--animation-time);
                }
                circle {
                    r: 0px;
                    fill: transparent;
                    stroke: black;
                    stroke-width: 0px;
                    transition: all var(--animation-time) ease-in-out;
                    transition-delay: calc(
                        var(--date-ratio) * var(--animation-time)
                    );
                }
            }
            .dates-axis {
                position: absolute;
                bottom: 0%;
                left: 30px;
                right: 10px;
                height: 20%;
                /* transition: opacity var(--animation-time) ease-in-out; */
                ul {
                    justify-content: space-between;
                    width: 100%;
                    list-style-type: none;
                    padding: 0;
                    margin: 0;
                    li {
                        position: absolute;
                        bottom: 0%;
                        left: calc(var(--date-ratio) * 100%);
                        display: block;
                        transform-origin: 0px 50%;
                        opacity: 0;
                        transform: rotate(30deg) translateY(100%);
                        transition: opacity var(--animation-time) ease-in-out,
                            transform var(--animation-time) ease-in-out;
                        transition-delay: calc(
                                var(--date-ratio) * var(--animation-time)
                            ),
                            calc(var(--date-ratio) * var(--animation-time));
                    }
                }
                svg {
                    position: absolute;
                    top: 0%;
                    left: 0%;
                    width: 100%;
                    height: 30%;
                    overflow: visible;
                    opacity: 0;
                    transition: opacity var(--animation-time) ease-in-out;
                    .axis {
                        stroke: black;
                        stroke-width: 2;
                        fill: none;
                    }
                    .tick {
                        stroke: black;
                        fill: none;
                        &.tick-type-0 {
                            stroke-width: 2px;
                        }
                        &.tick-type-1 {
                            stroke-width: 1px;
                        }
                        &.tick-type-2 {
                            stroke-width: 0.5px;
                        }
                    }
                }
                &.biggest-tick-0 {
                    li.tick-type-1 {
                        display: none;
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
                .dates-axis {
                    ul li {
                        opacity: 1;
                        transform: rotate(30deg) translateY(0%);
                    }
                    svg {
                        opacity: 1;
                    }
                }
                svg.chart {
                    top: 0%;
                    left: 30px;
                    right: 10px;
                    width: calc(100% - 40px);
                    height: 60%;
                    line {
                        stroke-width: 1px;
                        transition-delay: 0s;
                    }
                    .triangle-fill {
                        opacity: 0;
                        fill: transparent;
                    }
                    circle {
                        r: 3px;
                        fill: black;
                        &:hover {
                            stroke-width: 1px;
                        }
                        title {
                            color: red;
                        }
                    }
                }
            }

            .tooltip-anchor {
                position: absolute;
                top: 0px;
                left: 0px;
                width: 2px;
                height: 2px;
                opacity: 1;
                transition: top var(--animation-time) ease-in-out,
                    left var(--animation-time) ease-in-out;
                anchor-name: --tooltip-anchor;
                position: absolute;
            }
            .tooltip {
                display: block;
                position: absolute;
                position-anchor: --tooltip-anchor;
                background-color: white;
                border: 1px solid black;
                padding: 5px;
                border-radius: 5px;
                font-size: 12px;
                pointer-events: visible;
                opacity: 0;
                transition: opacity var(--animation-time) ease-in-out;
                position: absolute;
                position-area: bottom;
                width: 100px;
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

        var lines = [];
        for (var i = 0; i < this._points_list.length - 1; i++) {
            lines.push(
                i == 0
                    ? svg`
                <line
                    x1="${triangle_points[i].x}"
                    y1="${triangle_points[i].y}"
                    x2="${triangle_points[i + 1].x}"
                    y2="${triangle_points[i + 1].y}"
                    style="--date-ratio: ${this._points_list[i].x};"
                >
                    <animate
                        ${ref(this.first_in_animation)}
                        id="firstInAnimation"
                        dur="${MkBar.animation_time_in_s}s"
                        fill="freeze"
                        begin="indefinite"
                        attributeName="x1"
                        to="${this._points_list[i].x * 100.0}%"
                    ></animate>
                    <animate
                            dur="${MkBar.animation_time_in_s}s"
                            fill="freeze"
                            begin="firstInAnimation.begin+${
                                MkBar.animation_time_in_s *
                                this._points_list[i].x
                            }s"
                            class="in"
                            attributeName="y1"
                            to="${100 - this._points_list[i].y * 100.0}%"
                        ></animate>
                        <animate
                            dur="${MkBar.animation_time_in_s}s"
                            fill="freeze"
                            begin="firstInAnimation.begin+${
                                MkBar.animation_time_in_s *
                                this._points_list[i + 1].x
                            }s"
                            class="in"
                            attributeName="x2"
                            to="${this._points_list[i + 1].x * 100.0}%"
                        ></animate>
                        <animate
                            dur="${MkBar.animation_time_in_s}s"
                            fill="freeze"
                            begin="firstInAnimation.begin+${
                                MkBar.animation_time_in_s *
                                this._points_list[i + 1].x
                            }s"
                            class="in"
                            attributeName="y2"
                            to="${100 - this._points_list[i + 1].y * 100.0}%"
                        ></animate>

                    <animate
                        ${ref(this.first_out_animation)}
                        id="firstOutAnimation"
                        dur="${MkBar.animation_time_in_s}s"
                        fill="freeze"
                        begin="indefinite"
                        attributeName="x1"
                        to="${triangle_points[i].x}"
                    ></animate>
                    <animate
                            dur="${MkBar.animation_time_in_s}s"
                            fill="freeze"
                            begin="firstOutAnimation.begin+${
                                MkBar.animation_time_in_s *
                                this._points_list[i].x
                            }s"
                            class="out"
                            attributeName="y1"
                            to="${triangle_points[i].y}"
                        ></animate>
                        <animate
                            dur="${MkBar.animation_time_in_s}s"
                            fill="freeze"
                            begin="firstOutAnimation.begin+${
                                MkBar.animation_time_in_s *
                                this._points_list[i + 1].x
                            }s"
                            class="out"
                            attributeName="x2"
                            to="${triangle_points[i + 1].x}"
                        ></animate>
                        <animate
                            dur="${MkBar.animation_time_in_s}s"
                            fill="freeze"
                            begin="firstOutAnimation.begin+${
                                MkBar.animation_time_in_s *
                                this._points_list[i + 1].x
                            }s"
                            class="out"
                            attributeName="y2"
                            to="${triangle_points[i + 1].y}"
                        ></animate>
                </line>
            `
                    : svg`
                    <line
                        x1="${triangle_points[i].x}"
                        y1="${triangle_points[i].y}"
                        x2="${triangle_points[i + 1].x}"
                        y2="${triangle_points[i + 1].y}"
                        style="--date-ratio: ${this._points_list[i].x};"
                    >
                        <animate
                            dur="${MkBar.animation_time_in_s}s"
                            fill="freeze"
                            begin="firstInAnimation.begin+${
                                MkBar.animation_time_in_s *
                                this._points_list[i].x
                            }s"
                            class="in"
                            attributeName="x1"
                            to="${this._points_list[i].x * 100.0}%"
                        ></animate>
                        <animate
                            dur="${MkBar.animation_time_in_s}s"
                            fill="freeze"
                            begin="firstInAnimation.begin+${
                                MkBar.animation_time_in_s *
                                this._points_list[i].x
                            }s"
                            class="in"
                            attributeName="y1"
                            to="${100 - this._points_list[i].y * 100.0}%"
                        ></animate>
                        <animate
                            dur="${MkBar.animation_time_in_s}s"
                            fill="freeze"
                            begin="firstInAnimation.begin+${
                                MkBar.animation_time_in_s *
                                this._points_list[i + 1].x
                            }s"
                            class="in"
                            attributeName="x2"
                            to="${this._points_list[i + 1].x * 100.0}%"
                        ></animate>
                        <animate
                            dur="${MkBar.animation_time_in_s}s"
                            fill="freeze"
                            begin="firstInAnimation.begin+${
                                MkBar.animation_time_in_s *
                                this._points_list[i + 1].x
                            }s"
                            class="in"
                            attributeName="y2"
                            to="${100 - this._points_list[i + 1].y * 100.0}%"
                        ></animate>

                        <animate
                            dur="${MkBar.animation_time_in_s}s"
                            fill="freeze"
                            begin="firstOutAnimation.begin+${
                                MkBar.animation_time_in_s *
                                this._points_list[i].x
                            }s"
                            class="out"
                            attributeName="x1"
                            to="${triangle_points[i].x}"
                        ></animate>
                        <animate
                            dur="${MkBar.animation_time_in_s}s"
                            fill="freeze"
                            begin="firstOutAnimation.begin+${
                                MkBar.animation_time_in_s *
                                this._points_list[i].x
                            }s"
                            class="out"
                            attributeName="y1"
                            to="${triangle_points[i].y}"
                        ></animate>
                        <animate
                            dur="${MkBar.animation_time_in_s}s"
                            fill="freeze"
                            begin="firstOutAnimation.begin+${
                                MkBar.animation_time_in_s *
                                this._points_list[i + 1].x
                            }s"
                            class="out"
                            attributeName="x2"
                            to="${triangle_points[i + 1].x}"
                        ></animate>
                        <animate
                            dur="${MkBar.animation_time_in_s}s"
                            fill="freeze"
                            begin="firstOutAnimation.begin+${
                                MkBar.animation_time_in_s *
                                this._points_list[i + 1].x
                            }s"
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
                    style="--date-ratio: ${point.x};"
                    cx="${point.x * 100.0}%"
                    cy="${100 - point.y * 100.0}%"
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

        const dates_axis = this.render_dates_axis();

        return html` <div
            class="my-bar-chart"
            id="myBarChart"
            @mouseenter=${this.mouse_enter}
            @mouseleave=${this.mouse_leave}
            @focusin=${this.focus_in}
            @focusout=${this.focus_out}
            tabindex="0"
        >
            <div class="scale"></div>
            <svg class="chart">${triangle_fill} ${lines} ${circles}</svg>
            ${dates_axis}
            <div
                ${ref(this._tooltip_anchor_element)}
                class="tooltip-anchor"
            ></div>
            <div ${ref(this._tooltip_element)} class="tooltip">
                ${this._tooltip_content}
            </div>
        </div>`;
    }

    private render_dates_axis(): TemplateResult<1> {
        const min_date = this._list[0].date;
        const min_date_num = min_date.getTime();
        const max_date = this._list[this._list.length - 1].date;
        const diff = max_date.getTime() - min_date_num;

        const dates: [Date, DateType][] = [];
        var biggest_tick: DateType;

        if (diff > 0.5 * 365 * 24 * 60 * 60 * 1000) {
            biggest_tick =
                diff > 3 * 365 * 24 * 60 * 60 * 1000
                    ? DateType.Year
                    : DateType.Month;
            dates.push([min_date, DateType.Year]);
            var date = new Date(min_date.getFullYear(), min_date.getMonth(), 1);
            date = DatesHelpers.AddMonths(date, 1);
            while (date < max_date) {
                dates.push([
                    new Date(date),
                    date.getMonth() == 0 ? DateType.Year : DateType.Month,
                ]);
                date = DatesHelpers.AddMonths(date, 1);
            }
        } else {
            biggest_tick = DateType.Week;
            dates.push([min_date, DateType.Month]);
            var date = new Date(min_date.getFullYear(), min_date.getMonth(), 1);
            date = DatesHelpers.AddWeeks(date, 1);
            while (date < max_date) {
                dates.push([
                    new Date(date),
                    date.getDate() == 1
                        ? date.getMonth() == 0
                            ? DateType.Year
                            : DateType.Month
                        : DateType.Week,
                ]);
                date = DatesHelpers.AddWeeks(date, 1);
            }
        }
        return html`<div class="dates-axis biggest-tick-${biggest_tick}">
            <ul>
                ${dates.map(([date, dateType], _) => {
                    let dateString = '';
                    switch (dateType) {
                        case DateType.Year:
                            dateString = date.toLocaleDateString('he-IL', {
                                year: 'numeric',
                            });
                            break;
                        case DateType.Month:
                            dateString = date.toLocaleDateString('he-IL', {
                                month: '2-digit',
                                year: 'numeric',
                            });
                            break;
                        case DateType.Week:
                            dateString = date.toLocaleDateString('he-IL', {
                                month: '2-digit',
                                day: '2-digit',
                                year: '2-digit',
                            });
                            break;
                        case DateType.Day:
                            dateString = date.toLocaleDateString('he-IL', {
                                month: '2-digit',
                                day: '2-digit',
                                year: '2-digit',
                            });
                            break;
                    }
                    const ratio = (date.getTime() - min_date_num) / diff;
                    return html`<li
                        class="tick-type-${dateType.toString()}"
                        style="--date-ratio: ${ratio}"
                    >
                        ${dateString}
                    </li>`;
                })}
            </ul>
            <svg>
                <line class="axis" x1="0%" y1="50%" x2="100%" y2="50%"></line>
                ${dates.map(([date, dateType], _) => {
                    const x = (date.getTime() - min_date_num) / diff;
                    return svg`
                        <line
                            class="tick tick-type-${dateType.toString()}"
                            style="--date-ratio: ${x}"
                            x1="${x * 100}%"
                            y1="${dateType > 0 ? 5 : 0}0%"
                            x2="${x * 100}%"
                            y2="100%"
                        ></line>
                    `;
                })}
            </svg>
        </div>`; // TODO: implement the axis
    }

    private first_in_animation: Ref<SVGAnimateElement> = createRef();
    private first_out_animation: Ref<SVGAnimateElement> = createRef();
    private focus_within: boolean = false;

    // method for mouse enter
    private mouse_enter(e: MouseEvent): void {
        if (this.focus_within) return;
        this.first_in_animation.value?.beginElement();
    }
    private mouse_leave(e: MouseEvent): void {
        if (this.focus_within) return;
        this.first_out_animation.value?.beginElement();
    }
    private focus_in(e: FocusEvent): void {
        if (this.focus_within) return;
        this.first_in_animation.value?.beginElement();
        this.focus_within = true;
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
        this.first_out_animation.value?.beginElement();
    }

    private _tooltip_element: Ref<HTMLDivElement> = createRef();
    private _tooltip_anchor_element: Ref<HTMLDivElement> = createRef();
    private async show_tooltip(e: MouseEvent) {
        const target = e.target as SVGCircleElement;
        const tooltip = this._tooltip_element.value;
        const index = parseInt(target.getAttribute('data-index') || '0');
        const point = this.list[index];
        const formattedDate = point.date.toLocaleDateString('en-GB'); // Formats as DD/MM/YYYY
        this._tooltip_content = html`<div>
            ${formattedDate}, ${point.value.toFixed(2)}
        </div>`;
        if (this._tooltip_anchor_element.value) {
            this._tooltip_anchor_element.value.style.left = `${
                30 + target.cx.baseVal.value
            }px`;
            this._tooltip_anchor_element.value.style.top = `${target.cy.baseVal.value}px`;
        }
        // now await for the tooltip of the point
        if (point.tooltip) {
            this._tooltip_content = await point.tooltip.get_value();
        }
    }
}

declare global {
    interface HTMLElementTagNameMap {
        'mk-bar': MkBar;
    }
}
