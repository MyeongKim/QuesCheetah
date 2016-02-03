import "qc-sdk";

export default function Config(){
    var config = {
        'apiKey': 'ee9c63a4b947cdbc2b6759e655c7e175a8a1dca2',
        'callBackUrl': 'http://localhost:8000',
    };
    var qc = new QuesCheetah(config);
}