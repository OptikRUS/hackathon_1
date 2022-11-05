export abstract class Field {
    public abstract key: string
    public abstract name: string

    constructor(public rawValue: any) {
    }

    abstract isValid(): boolean

    abstract getValue(): any
}
