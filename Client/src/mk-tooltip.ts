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

    static styles = css`
        :host {
            height: 4em;
            width: 8em;
            display: grid;
            grid-template-columns: auto 2fr;
            grid-template-rows: auto auto;
            grid-template-areas:
                'img name'
                'img link';
        }
        img {
            grid-area: img;
            view-transform-name: sharon;
            height: 100%;
        }
        h6 {
            grid-area: name;
        }
        a {
            grid-area: link;
        }
    `;

    override render() {
        return html`
            <img src="${this.image}" alt="${this.name}" />
            <h6>${this.name}</h6>
            <a href="../mk?id=${this.mkId}">פתח חבר כנסת</a>
        `;
    }
}

declare global {
    interface HTMLElementTagNameMap {
        'mk-tooltip': MkTooltip;
    }
}
