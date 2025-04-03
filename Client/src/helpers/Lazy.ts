export class Lazy<T> {
    private _value: T | undefined = undefined;
    private _isInitialized = false;
    private _initializer: Promise<T> | (() => T);
    
    constructor(initializer: Promise<T> | (() => T)) {
        if (typeof initializer !== "function" && !(initializer instanceof Promise)) {
            throw new Error("Initializer must be a function or a Promise");
        }
        this._initializer = initializer;
    }
    
    public async get_value(): Promise<T> {
        if (!this._isInitialized) {
            if (this._initializer instanceof Promise) {
                this._value = await this._initializer;
            } else {
                this._value = this._initializer();
            }
            this._isInitialized = true;
        }
        return this._value as T;
    }

    public reset(): void {
        this._isInitialized = false;
        this._value = undefined;
    }
}