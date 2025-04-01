import { css, html, LitElement } from 'lit';
import { customElement, property } from 'lit/decorators.js';
import { MkBar, SpeechPoint } from './mk-bar';

@customElement('my-element')
export class MyElement extends LitElement {
    static styles = css`
        div {
            margin: 30px;
        }
    `;

    private static randomInt(min: number, max: number): number {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    private static create_random_list(): SpeechPoint[] {
        const list: SpeechPoint[] = [];
        const length = MyElement.randomInt(5, 20); // Random length between 5 and 20
        for (let i = 0; i < length; i++) {
            const date = new Date(
                MyElement.randomInt(2000, 2023),
                MyElement.randomInt(1, 12) - 1, // Month (0-11 for JavaScript Date)
                MyElement.randomInt(1, 28) // Day of the month (1-28 to avoid issues with months)
            );
            const value = Math.random(); // Random value between 0 and 1
            list.push(new SpeechPoint(date, value));
        }
        return list;
    }

    override render() {
        // const list: SpeechPoint[] = [
        //     new SpeechPoint(new Date(2000, 1, 1), 0),
        //     new SpeechPoint(new Date(2001, 1, 1), 0.1),
        //     new SpeechPoint(new Date(2002, 1, 1), 0.5),
        //     new SpeechPoint(new Date(2003, 1, 1), 0.2),
        //     new SpeechPoint(new Date(2004, 1, 1), 0.9),
        //     new SpeechPoint(new Date(2005, 1, 1), 1),
        //     new SpeechPoint(new Date(2006, 1, 1), 0.8),
        //     new SpeechPoint(new Date(2007, 1, 1), 0.6),
        //     new SpeechPoint(new Date(2008, 1, 1), 0.3),
        //     new SpeechPoint(new Date(2009, 1, 1), 0),
        //     new SpeechPoint(new Date(2010, 1, 1), 0.5),
        // ];
        return html`
            <div>
                <mk-bar
                    average="${MyElement.randomInt(1, 5)}"
                    .list=${MyElement.create_random_list()}
                ></mk-bar>
            </div>
            <div>
                <mk-bar
                    average="${MyElement.randomInt(1, 5)}"
                    .list=${MyElement.create_random_list()}
                ></mk-bar>
            </div>
            <div>
                <mk-bar
                    average="${MyElement.randomInt(1, 5)}"
                    .list=${MyElement.create_random_list()}
                ></mk-bar>
            </div>
        `;
    }
}
