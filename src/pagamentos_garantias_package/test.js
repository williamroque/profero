const { spawn } = require('child_process');

const subprocess = spawn('python', ['main.py']);

const input = {
    'primeira-serie': 16,
    'date': 'set/2020',
    'output-path': '/Users/jetblack-work/Desktop/slideshow.pptx',
    'project-logo': '/Users/jetblack-work/Desktop/project_logo.png',
    'client-logo': '/Users/jetblack-work/Desktop/client_logo.png',
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
                    'juros': .085
                    'data-emissao': '12/03/2020',
                    'vencimento': '07/08/2026',
                    'valor-emissao': 25.9 * 1_000_000,
                    'saldo-devedor': 14.02 * 1_000_000
                },
                '17': {
                    'instrumento-financeiro': '18C0722263',
                    'isin': 'BRLGOSCRI0E9',
                    'cedente': 'Paysage',
                    'correcao': 'IPCA',
                    'juros': .135
                    'data-emissao': '12/03/2020',
                    'vencimento': '07/05/2031',
                    'valor-emissao': 11.1 * 1_000_000,
                    'saldo-devedor': 8.73 * 1_000_000
                }
            }
        }
    ]
};

subprocess.stdin.write(JSON.stringify(input));
subprocess.stdin.end();

subprocess.stderr.on('data', err => {
    console.log(err.toString());
});

subprocess.stdout.on('data', out => {
    console.log(out.toString());
});
