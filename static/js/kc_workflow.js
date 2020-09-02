function kc_workflow (approvalStatus) {
    console.log(111111111111)

    var tenantcode = document.querySelectorAll('#tenantcode')[1].value,   //获得选中的值
        environment = document.querySelectorAll('#environment')[1].value,   //获得选中的值
        businessType = document.querySelector('#businessType').value,
        title = document.querySelector('#title').value;
    if (tenantcode != '' & environment != '' & title != '' & businessType != '') {
        setTimeout(function () {
            $.ajax({
                type: "post",
                url: "/tool/ChangeK2TravelWorkflowStatus",
                dataType: "json",
                data: {
                    "tenantcode" : tenantcode,
                    "environment": environment,
                    "businessType": businessType,
                    "title": title,
                    "approvalStatus": approvalStatus,
                },
                success: function (data) {
                    var str = JSON.stringify(data);
                    alert(approvalStatus + "成功" + str);
                },
                error: function (XMLHttpRequest, textStatus, errorThrown) {
                    document.getElementById("req").value = XMLHttpRequest.statusText + " " + XMLHttpRequest.status + ":\n" + XMLHttpRequest.responseText
                    layer.close(loading)
                }
            });
        });
    }
};

function supplier_workflow (approvalStatus) {
    console.log(222222222)
    var tenantcode = document.querySelectorAll('#tenantcode')[2].value,   //获得选中的值
        environment = document.querySelectorAll('#environment')[2].value,   //获得选中的值
    // var tenantcode = $("#tenantcode option:selected").val(),  //获得选中的值
    //     environment = document.querySelectorAll("#environment")[2].value, //获得选中的值
        operation = $("#operation option:selected").val(),
        // businessType = $("#businessType option:selected").val(),
        // console.log(businessType)
        supplier_name = document.getElementById("supplier_name").value;

    if (tenantcode != '' & environment != '' & title != '' & businessType != '') {
        setTimeout(function () {
            $.ajax({
                type: "post",
                url: "/tool/ChangeK2SupplierWorkflowStatus",
                dataType: "json",
                data: {
                    "tenantcode" : tenantcode,
                    "environment": environment,
                    // "businessType": businessType,
                    "supplier_name": supplier_name,
                    "operation": operation,
                    "approvalStatus": approvalStatus,
                },
                success: function (data) {
                    var str = JSON.stringify(data);
                    alert(approvalStatus + "成功" + str);
                },
                error: function (XMLHttpRequest, textStatus, errorThrown) {
                    document.getElementById("req").value = XMLHttpRequest.statusText + " " + XMLHttpRequest.status + ":\n" + XMLHttpRequest.responseText
                    layer.close(loading)
                }
            });
        });
    }
};
