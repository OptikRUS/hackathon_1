import {toast} from "react-toastify";
import {Field} from "./abc";

export class SendRequest {
    public fields: Field[] = []

    private dataForSubmit: Record<string, any> = {}

    public allFieldsIsValid(): boolean {
        for (const field of this.fields) {
            if (!field.isValid()) {

                toast.error(`Поле ${field.name} не валидно`)

                return false
            }
        }

        return true
    }

    private collectData() {
        this.fields.forEach(field => {
            this.dataForSubmit[field.key] = field.getValue()
        })
    }

    public send() {
        if (this.allFieldsIsValid()) {
            this.collectData()
            console.log(`send ${JSON.stringify(this.dataForSubmit)}`)
        }
    }
}
