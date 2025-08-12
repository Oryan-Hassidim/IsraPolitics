import { LitElement, TemplateResult, css, html, svg } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';

@customElement('mk-tooltip')
export class MkTooltip extends LitElement {
    @property({ type: Number })
    mkId: number = 0;

    @property({ type: String })
    name: string = '';

    @property({ type: String })
    image: string = '';

    @property({ type: String })
    innerHTML: string = '';

    static styles = css`
        :host {
            height: min-content;
            width: fit-content;
            display: grid;
            grid-template-columns: auto auto;
            grid-template-rows: auto auto auto;
            grid-template-areas:
                'img name'
                'img innerHTML'
                'img link';
            direction: rtl;
            padding: 1em;
            column-gap: 0.5em;
            background-color: #f1f4fd;
            border: 1px solid black;
            border-radius: 0.5em;
            box-shadow: 0px 4px 10px 4px #ccdbff;
        }
        img {
            grid-area: img;
            view-transform-name: sharon;
            height: 8em;
        }
        .name {
            grid-area: name;
            margin: 0;
        }
        a {
            grid-area: link;
        }
        .innerHTML {
            grid-area: innerHTML;
        }
    `;

    override render() {
        return html`
            <img src="${this.image}" alt="${this.name}" />
            <h3 class="name">${this.name}</h3>
            <a href="../mk?id=${this.mkId}">פתח חבר כנסת</a>
            <div class="innerHTML" .innerHTML=${this.innerHTML}></div>
        `;
    }
}

declare global {
    interface HTMLElementTagNameMap {
        'mk-tooltip': MkTooltip;
    }
}
