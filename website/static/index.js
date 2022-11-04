function deleteAcc(accID){
    fetch("/delete-acc",{
        method: "POST",
        body: JSON.stringify({ accID: accID }),
    }).then((_res) => {
        window.location.href = "/accounts";
    });
}

function deleteIP(ipAddress){
    fetch("/delete-ip",{
        method: "POST",
        body: JSON.stringify({ ipAddress: ipAddress }),
    }).then((_res) => {
        window.location.href = "/";
    });
}