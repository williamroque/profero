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
