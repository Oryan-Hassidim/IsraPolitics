import { css, html, LitElement } from 'lit';
import { customElement, property } from 'lit/decorators.js';
import { SpeechPoint } from './mk-bar';
import { MkView } from './mk-view';

@customElement('my-element')
export class MyElement extends LitElement {
    static styles = css`
        :root {
            width: 100%;
            height: 100vh;
        }
    `;

    // private static randomInt(min: number, max: number): number {
    //     return Math.floor(Math.random() * (max - min + 1)) + min;
    // }

    // private static create_random_list(): SpeechPoint[] {
    //     const list: SpeechPoint[] = [];
    //     const length = MyElement.randomInt(5, 20); // Random length between 5 and 20
    //     for (let i = 0; i < length; i++) {
    //         const date = new Date(
    //             MyElement.randomInt(2000, 2023),
    //             MyElement.randomInt(1, 12) - 1, // Month (0-11 for JavaScript Date)
    //             MyElement.randomInt(1, 28) // Day of the month (1-28 to avoid issues with months)
    //         );
    //         const value = Math.random(); // Random value between 0 and 1
    //         list.push(new SpeechPoint(date, value));
    //     }
    //     return list;
    // }

    override render() {
        return html`
            <mk-view mkId="12956"></mk-view>
        `;
    }
}

declare global {
    interface HTMLElementTagNameMap {
        'my-element': MyElement;
    }
}
