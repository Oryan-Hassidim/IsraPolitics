export enum DateType {
    Year,
    Month,
    Week,
    Day,
}

export class DatesHelpers {
    public static ToShortDate(date: Date): string {
        return date.toLocaleDateString('he-IL', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
        });
    }

    public static AddYears(date: Date, years: number): Date {
        date.setFullYear(date.getFullYear() + years);
        return date;
    }
    public static AddMonths(date: Date, months: number): Date {
        date.setMonth(date.getMonth() + months);
        return date;
    }
    public static AddWeeks(date: Date, weeks: number): Date {
        date.setDate(date.getDate() + weeks * 7);
        return date;
    }
    public static AddDays(date: Date, days: number): Date {
        date.setDate(date.getDate() + days);
        return date;
    }
}
