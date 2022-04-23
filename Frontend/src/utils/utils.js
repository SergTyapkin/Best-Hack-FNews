export function getChildrenHeight(el) {
    const children = Array.from(el.children);
    let res = 0;
    if (!children)
        return res;
    children.forEach((child) => {
        res += child.scrollHeight;
    })
    return res;
}

const _timedTimeouts = [];
export function setTimedClass(elements, className, timeout = 1500) {
    _timedTimeouts.forEach((timeout, idxTime) => {
        elements.forEach((el, idxEl) => {
            if (el === timeout.element) {
                clearTimeout(timeout.timeout);
                _timedTimeouts.splice(idxTime, 1);
            }
        });
    });
    elements.forEach(element => {
        element.classList.add(className);

        _timedTimeouts.push({
            element: element,
            timeout: setTimeout(() => element.classList.remove(className), timeout)
        });
    });
}

export function deepClone(obj = {}) {
    return JSON.parse(JSON.stringify(obj));
}

export function curNameToSymbol(currencyName) {
    let sym = {
        aud: '$',
        azn: '',
        gbp: '£',
        amd: '֏',
        byn: '',
        bgn: '',
        brl: '',
        huf: '',
        hkd: '$',
        dkk: '',
        usd: '$',
        eur: '€',
        inr: '₹',
        kzt: '₸',
        cad: '$',
        kgs: '',
        cny: '¥',
        mdl: '',
        nok: '',
        pln: '',
        ron: '',
        xdr: '',
        sgd: '$',
        tjs: '',
        try: '₺',
        tmt: '',
        uzs: '',
        uah: '₴',
        czk: '',
        sek: '',
        chf: '',
        zar: '',
        krw: '₩',
        jpy: '¥',
    }[currencyName.toLowerCase()];
    if (sym === '')
        sym = currencyName.toUpperCase();

    return sym;
}
