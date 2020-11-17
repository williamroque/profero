const { spawn } = require('child_process');

// A ideia aqui é simular o modo de executar do GENSEC
const subprocess = spawn('python', ['main.py']);

const MM = 1_000_000;

// O formato deste objeto deve refletir o gerado automaticamente pelo GENSEC
const input = {
    'primeira-serie': 16,
    'output-path': '/Users/jetblack-work/Desktop/slideshow.pptx',
    'project-logo': '/Users/jetblack-work/Desktop/project_logo.png',
    'client-logo': '/Users/jetblack-work/Desktop/client_logo.png',
    slides: [
        {
            id: 'title',
            inputs: {
                'date': '07/09/2020',
            }
        },
        {
            id: 'disclaimer',
            inputs: {
                'date': '07/09/2020',
            }
        },
        {
            id: 'table-of-contents',
            inputs: {
                'date': '07/09/2020',
            }
        },
        {
            id: 'dados-operacao',
            inputs: {
                'date': '07/09/2020',
                '16': {
                    'instrumento-financeiro': '18C0722274',
                    'isin': 'BRLGOSCRI0D1',
                    'cedente': 'Paysage',
                    'correcao': 'IPCA',
                    'juros': .085,
                    'data-emissao': '12/03/2020',
                    'vencimento': '07/08/2026',
                    'valor-emissao': 25.9 * MM,
                    'saldo-devedor': 14022391.9770339
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
                    'saldo-devedor': 8727080.6117798
                }
            }
        },
        {
            id: 'garantia',
            inputs: {
                'date': '07/09/2020',
                'fundo-reserva': .9 * MM,
                'estoque': 34980928.786,
                'direitos-creditorios-inadimplidos':  17357683.41,
                'direitos-creditorios-adimplidos': 32603090.28,
                'garantia-minima':  26161893.4771358,
                'gatilho-sobregarantia': 32603090.28,
            }
        },
        {
            id: 'pagamento-investidores',
            inputs: {
                'date': '07/09/2020',
                'numero-evento': 30,
                '16': {
                    'quantidade': 2590,
                    'juros-unitarios': 38.36501884,
                    'amortizacao-unitaria': 67.45591265,
                    'amex-unitaria': 142.63125483,
                    'pagamento-total-unidade': 248.45218632,
                    'pagamento-investidores': 591316.20,
                    'investidores': [
                        108325.15,
                        433300.61,
                        49690.44,
                    ],
                },
                '17': {
                    'quantidade': 1110,
                    'juros-unitarios': 85.60461563,
                    'amortizacao-unitaria': 0,
                    'amex-unitaria': 207.12779279,
                    'pagamento-total-unidade': 292.73240842,
                    'pagamento-investidores': 298587.06,
                    'investidores': [
                        59717.41,
                        238869.65,
                        0,
                    ],
                }
            }
        },
        {
            id: 'ativos-imobiliarios',
            inputs: {
                'date': '07/09/2020',
            }
        },
        {
            id: 'caracteristicas-ativos',
            inputs: {
                'date': '07/09/2020',
            }
        },
        {
            id: 'direitos-creditorios-garantia',
            inputs: {
                'date': '07/09/2020',
                'empreendimentos': [
                    'Araçari',
                    'Tangará',
                    'Aranguá',
                    'Araguari',
                ],
                'contratos': [
                    107,
                    127,
                    170,
                    77,
                ],
                'num-direitos-adimplidos': [
                    81,
                    90,
                    116,
                    68,
                ],
                'num-direitos-inadimplidos': [
                    26,
                    37,
                    54,
                    9,
                ],
                'direitos-adimplidos': [
                    6.86,
                    7.58,
                    11.59,
                    6.58,
                ],
                'direitos-inadimplidos': [
                    3.35,
                    4.96,
                    8.09,
                    0.96,
                ]
            }
        }
    ]
};

// Escrever o objeto de dados ao stdin do programa
subprocess.stdin.write(JSON.stringify(input));
subprocess.stdin.end();

// Escrever erros do programa ao stderr (para poder bifurcar a saída)
subprocess.stderr.on('data', err => {
    process.stderr.write(err.toString());
    process.exit(1)
});

// Escrever stdout do programa ao stdout
subprocess.stdout.on('data', out => {
    console.log(out.toString());
});
