import { LitElement, html, css } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';
import { MkData, MkTopicData, SpeechDay } from './helpers/MkData';
import './mk-bar';
import groupBy from './helpers/GroupBy';

// TODO: https://knesset.gov.il/WebSiteApi/knessetapi/MKs/GetMkdetailsHeader?mkId=125&languageKey=he
// TODO: https://knesset.gov.il/WebSiteApi/knessetapi/MKs/GetGovrnmentActivity?mkId=125&lnaguageKey=he

interface CsvRecord {
    Id: number; // Unique identifier for the record
    Date: string; // Date of the record
    Topic: string; // Topic name
    Text: string; // Text content of the record
    Rank: number; // Rank or score associated with the record
}

@customElement('mk-view')
export class MkView extends LitElement {
    @property({ type: Number })
    public mkId: number = -1;

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
                margin: 0;
            }
            h2 {
                grid-area: description;
                font-size: 1.2em;
                font-weight: 100;
            }
            img {
                grid-area: image;
                width: 100%;
                height: auto;
                box-shadow: 6px -6px 6px rgba(0, 0, 0, 0.5);
                view-transition-name: sharon;
            }
            a {
                grid-area: knesset-site;
            }
            .topics {
                grid-area: topics;
                display: flex;
                flex-direction: column;
                gap: 30px;
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
                    >קרא עוד באתר הכנסת</a
                >
                <div class="topics">
                    ${this._mkData.Topics.map(
                        (topic) =>
                            html`
                                <div class="topic">
                                    <h3>${topic.topicName}</h3>
                                    <mk-bar
                                        .average=${topic.average}
                                        .list=${topic.records}
                                    ></mk-bar>
                                </div>
                                <div class="topic">
                                    <h3>פתרון שתי המדינות</h3>
                                    <mk-bar
                                        average="6.5"
                                        .list=${topic.records}
                                    ></mk-bar>
                                </div>
                                <div class="topic">
                                    <h3>הפרדת דת ממדינה</h3>
                                    <mk-bar
                                        average="5.5"
                                        .list=${topic.records}
                                    ></mk-bar>
                                </div>
                                <div class="topic">
                                    <h3>הגבלות על ייבוא</h3>
                                    <mk-bar
                                        average="7"
                                        .list=${topic.records}
                                    ></mk-bar>
                                </div>
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
        const response = await fetch(
            `./client_data/mk_data/${this.mkId}/main.json`
        );
        if (response.ok) {
            const data = await response.json();
            const temp = new MkData(
                data.id,
                data.knessetSiteId,
                data.name,
                data.imageUrl,
                data.description,
                data.Topics.map(
                    (topic: any) =>
                        new MkTopicData(
                            topic.topicName,
                            topic.average
                            // topic.speechesId,
                            // topic.dates.map((date: string) => new Date(date)),
                            // topic.ranks
                        )
                )
            );
            for (const topic of temp.Topics) {
                const topicResponse = await fetch(
                    `client_data/mk_data/${this.mkId}/${topic.topicName}.csv`
                );
                // Id,Date,Topic,Text,Rank
                // read as csv
                if (topicResponse.ok) {
                    const text = await topicResponse.text();
                    const records: Array<CsvRecord> = Papa.parse(text, {
                        header: true,
                        skipEmptyLines: true,
                        dynamicTyping: true,
                    }).data;
                    topic.records = groupBy(records, (r) => r.Date).map(
                        (group) => {
                            const date = new Date(group.key);
                            const ranks = group.items.map((item) => item.Rank);
                            const average =
                                ranks.reduce((a, b) => a + b, 0) / ranks.length;
                            return new SpeechDay(
                                date,
                                average,
                                group.items
                                    .map(
                                        (item) =>
                                            `${item.Topic}: ${item.Text} (${item.Rank})`
                                    )
                                    .join('\n')
                            );
                        }
                    );
                } else {
                    console.error(
                        'Error fetching topic data:',
                        topicResponse.statusText
                    );
                }
            }
            this._mkData = temp;
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
