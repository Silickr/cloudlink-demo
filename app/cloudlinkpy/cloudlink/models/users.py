# -*- coding: UTF-8 -*-
class Users(object):

    def __init__(self, user_status,
                 userId, deptCode, mobileNumber,
                 usernameCn, usernameEn, sex,
                 corpUserId, userEmail, secretary,
                 phoneNumber, address, remark):
        self.user_status = user_status
        self.userId = userId
        self.deptCode = deptCode
        self.mobileNumber = mobileNumber
        self.usernameCn = usernameCn
        self.usernameEn = usernameEn
        self.gender = sex
        self.corpUserId = corpUserId
        self.userEmail = userEmail
        self.secretary = secretary
        self.phoneNumber = phoneNumber
        self.address = address
        self.remark = remark