import { LitElement, html, css } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';
import { MkData, MkTopicData } from './helpers/MkData';
import { SpeechPoint } from './mk-bar';

@customElement('mk-view')
export class MkView extends LitElement {
    @property({ type: Number })
    public mkId: number;

    @state()
    private _mkData: MkData = new MkData(0, 0, '', '', '', []);

    public static styles = css`
        .mk-view {
            direction: rtl;
            display: grid;
            grid-template-areas:
                'image topics'
                'name topics'
                'description topics'
                'knesset-site topics';
            grid-template-columns: 1fr 2fr;
            grid-template-rows: auto auto auto auto;
            column-gap: 40px;
            padding: 40px 20px;

            h1 {
                grid-area: name;
            }
            h2 {
                grid-area: description;
            }
            img {
                grid-area: image;
                width: 100%;
                height: auto;
            }
            a {
                grid-area: knesset-site;
            }
            .topics {
                grid-area: topics;
                display: flex;
                flex-direction: column;
                /* gap: 30px; */

                mk-bar {
                    margin-bottom: 30px;
                }
            }
        }
    `;

    override render() {
        return html`
            <div class="mk-view">
                <img
                    src="${this._mkData.imageUrl}"
                    alt="${this._mkData.name}"
                />
                <h1>${this._mkData.name}</h1>
                <h2>${this._mkData.description}</h2>
                <a
                    href="https://main.knesset.gov.il/mk/apps/mk/mk-positions/${this
                        ._mkData.knessetSiteId}"
                    >אתר הכנסת</a
                >
                <div class="topics">
                    ${this._mkData.Topics.map(
                        (topic) =>
                            html`
                                <h3>${topic.topicName}</h3>
                                <mk-bar
                                    .average=${topic.average}
                                    .list=${topic.dates.map(
                                        (date, index) =>
                                            new SpeechPoint(
                                                date,
                                                topic.ranks[index]
                                            )
                                    )}
                                ></mk-bar>
                            `
                    )}
                </div>
            </div>
        `;
    }

    public override async connectedCallback(): Promise<void> {
        super.connectedCallback();
        await this.fetchData();
    }

    private async fetchData(): Promise<void> {
        const response = await fetch(`client_data/mk_data/${this.mkId}.json`);
        if (response.ok) {
            const data = await response.json();
            this._mkData = new MkData(
                data.id,
                data.knessetSiteId,
                data.name,
                data.imageUrl,
                data.description,
                data.Topics.map(
                    (topic: any) =>
                        new MkTopicData(
                            topic.topicName,
                            topic.average,
                            topic.speechesId,
                            topic.dates.map((date: string) => new Date(date)),
                            topic.ranks
                        )
                )
            );
        } else {
            console.error('Error fetching MK data:', response.statusText);
        }
    }
}

declare global {
    interface HTMLElementTagNameMap {
        'mk-view': MkView;
    }
}
