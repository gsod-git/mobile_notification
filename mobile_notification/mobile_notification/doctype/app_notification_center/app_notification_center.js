// Copyright (c) 2018, Tridots Tech and contributors
// For license information, please see license.txt
var valuesDocss = [];

frappe.ui.form.on('App Notification Center', {

    refresh: function(frm) {
        frappe.breadcrumbs.add("Setup");
        cur_frm.set_value('url', 'General')
        cur_frm.set_value('message', '')
        cur_frm.set_value('content_data', '')
        cur_frm.set_value('member_list', '')
    },
    create_receiver_list: function(frm) {


    },
    get_list: function(frm) {
        valuesDocss = [];
        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "Member",
                order_by: "member_name",
                fields: ["player_id", "member_name", 'name'],
                filters: [
                    ["player_id", "!=", " "]
                ],
                limit_page_length: 1000
            },
            callback: function(r) {
                if (r.message) {
                    var a = '';
                    var b = '';
                    console.log(r.message)
                    for (var i = 0; i < r.message.length; i++) {
                        a += r.message[i].player_id + '\n';
                        frm.set_value('receiver_list', a)
                    }
                    for (var i = 0; i < r.message.length; i++) {
                        b += r.message[i].name + ' - ' + r.message[i].member_name + '\n';
                        frm.set_value('member_list', b)
                    }
                    for (var i = 0; i < r.message.length; i++) {
                        var memberdata = {
                            member: r.message[i].name,
                            member_name: r.message[i].member_name
                        }
                        valuesDocss.push(memberdata)                  
                        console.log(valuesDocss)
                    }
                    for(var i=0;i<valuesDocss.length;i++){
                        console.log(valuesDocss[i])
                    }
                }
            }
        });
    },

    send_notification: function(frm) {
        console.log(frm.doc.items)
        if (frm.doc.url != 'General') {
            if (frm.doc.items != '' && frm.doc.items != undefined) {
                send(frm)
            } else {
                frappe.msgprint('Please select Redirect Url')
            }
        } else {
            send(frm)
        }
    },

});
var send = function(frm) {
    var a = frm.doc.receiver_list.split("\n");
    var b = a.filter(function(v) { return v !== '' });
    frappe.call({
        "method": "frappe.client.get",
        args: {
            doctype: "App Notification Settings",
        },
        callback: function(r) {
            var receiver = frm.doc.receiver_list.split("\n");
            var one_signal_userconfig = {
                headers: {
                    'Content-Type': 'application/json',
                    "Authorization": "Basic " + r.message.secret_key
                }
            };
            var info = {};
            var user_notification_data = {
                "app_id": r.message.app_id,
                "contents": { "en": frm.doc.content_data },
                "data": { "add_data": frm.doc.message, "url": frm.doc.url + "/" + frm.doc.items },
                "include_player_ids": b
            }
            $.post(r.message.notification_gateway_url, user_notification_data, one_signal_userconfig).done(function(e) { console.log(e); });
            var url;
            if (frm.doc.url == 'General') {
                url = frm.doc.url
            } else {
                url = frm.doc.url + "/" + frm.doc.items
            }
            frappe.call({
                method: "mobile_notification.mobile_notification.doctype.app_notification_center.app_notification_center.insert_notification",
                args: {
                    name: frm.doc.content_data,
                    message: frm.doc.message,
                    url: url,
                    table_5: valuesDocss
                },
                callback: function(Responseresult) {
                    console.log(Responseresult)
                    // $(".tblQty").each(function() {
                    //     if (parseInt($(this).val()) > 0) {
                    //         var valueObj = {
                    //             "doctype": "TourBookingTickets",
                    //             "person_type": $(this).parent().parent().find("td:eq(0)").text(),
                    //             "quantity": $(this).val(),
                    //             "parenttype": "TourBookings",
                    //             "parentfield": "persons",
                    //             "unit_price": $(this).parent().parent().attr("unitprice"),
                    //             "total_price": $(this).parent().parent().find(".tblAmt").text(),
                    //             "parent": EntryName,
                    //         };
                    //         valuesDocss.push(valueObj);
                    //     }
                    // });
                    frappe.msgprint('Notification Sent Successfully');
                    cur_frm.set_value('member_list', null);
                    cur_frm.set_value('message', null);
                    cur_frm.set_value('content_data', "General");
                    cur_frm.set_value('url', null);
                    cur_frm.set_value('items', null);
                }
            });

        }
    });
}
// frappe.ui.form.on("App Notification Center", "refresh", function(frm) {
//     cur_frm.set_query("items", function(s) {
//         // frappe.call({
//         //     method: "frappe.client.get_list",
//         //     args: {
//         //         doctype: frm.doc.events,
//         //         fields: ['name']

//         //     },
//         //     callback: function(r) {
//         //         if (r.message) {
//         //             frm.set_value(r.message)
//         //             // var a = '';
//         //             // var b = '';
//         //             // for (var i = 0; i < r.message.length; i++) {
//         //             //     a += r.message[i].player_id + '\n';
//         //             //     frm.set_value('events', a)
//         //             // }
//         //             // for (var i = 0; i < r.message.length; i++) {
//         //             //     b +=r.message[i].name +' - '+ r.message[i].member_name + '\n';
//         //             //     frm.set_value('member_list', b)
//         //             // }
//         //         }
//         //     }
//         // });
//         return {
//             "filters": {
//                 "sponsorship_type": (frm.doc.url)
//             }
//         };
//     });
// });
frappe.ui.form.on('App Notification Center', 'url', function(frm, cdt, cdn) {
    if (frm.doc.url) {
        frappe.call({
            method: 'mobile_notification.mobile_notification.doctype.app_notification_center.app_notification_center.get_items',
            args: {
                url: frm.doc.url
            },
            callback: function(data) {
                var html = '';
                console.log(data.message)
                if (data.message == undefined) {
                    $('select[data-fieldname=items]').html(html)
                    $('select[data-fieldname=items]').parent().parent().parent().parent().hide()
                } else if (data.message.length > 0) {
                    html = '<option></option>'
                    if (frm.doc.sponsorship_type == 'Samaj Darshan') {
                        for (var i = 0; i < data.message.length; i++) {
                            var list = data.message[i].list;
                            for (var j = 0; j < list.length; j++) {
                                var value = list[j].month + '-' + data.message[i].year;
                                html += '<option value="' + value + '">' + value + '</option>';
                            }
                        }
                    } else {
                        for (var i = 0; i < data.message.length; i++) {
                            html += '<option value="' + data.message[i].name + '">' + data.message[i].name + '</option>';
                        }
                    }

                    $('select[data-fieldname=items]').html(html)
                    $('select[data-fieldname=items]').parent().parent().parent().parent().show()
                } else {
                    $('select[data-fieldname=items]').parent().parent().parent().parent().hide()
                }
            }
        })
    }
})