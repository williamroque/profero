const { spawn } = require('child_process');

const subprocess = spawn('python', ['main.py']);

const MM = 1_000_000;

const input = {
    'primeira-serie': 16,
    'date': '07/09/2020',
    'output-path': '/Users/jetblack-work/Desktop/slideshow.pptx',
    'project-logo': '/Users/jetblack-work/Desktop/project_logo.png',
    'client-logo': '/Users/jetblack-work/Desktop/client_logo.png',
    'saldo-cri': 21973702.7683875,
    slides: [
        {
            id: 'title',
            inputs: {}
        },
        {
            id: 'disclaimer',
            inputs: {}
        },
        {
            id: 'table-of-contents',
            inputs: {}
        },
        {
            id: 'dados-operacao',
            inputs: {
                '16': {
                    'instrumento-financeiro': '18C0722274',
                    'isin': 'BRLGOSCRI0D1',
                    'cedente': 'Paysage',
                    'correcao': 'IPCA',
                    'juros': .085,
                    'data-emissao': '12/03/2020',
                    'vencimento': '07/08/2026',
                    'valor-emissao': 25.9 * MM,
                    'saldo-devedor': 0.616383167666443
                },
                '17': {
                    'instrumento-financeiro': '18C0722263',
                    'isin': 'BRLGOSCRI0E9',
                    'cedente': 'Paysage',
                    'correcao': 'IPCA',
                    'juros': .135,
                    'data-emissao': '12/03/2020',
                    'vencimento': '07/05/2031',
                    'valor-emissao': 11.1 * MM,
                    'saldo-devedor': 0.383616832333557
                }
            }
        },
        {
            id: 'garantia',
            inputs: {
                'fundo-reserva': .9 * MM,
                'estoque': 34980928.786,
                'direitos-creditorios-inadimplidos':  17357683.41,
                'direitos-creditorios-adimplidos': 32603090.28,
                'garantia-minima': 25269758.1836456
            }
        }
    ]
};

subprocess.stdin.write(JSON.stringify(input));
subprocess.stdin.end();

subprocess.stderr.on('data', err => {
    process.stderr.write(err.toString());
    process.exit(1)
});

subprocess.stdout.on('data', out => {
    console.log(out.toString());
});
