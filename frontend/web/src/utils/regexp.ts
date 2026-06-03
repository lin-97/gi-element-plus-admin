/** 中国大陆 11 位手机号（空值不校验） */
export const PHONE_REG = /^\s*(?:$|1[3-9]\d{9})\s*$/

/** 邮箱地址（空值不校验） */
export const EMAIL_REG = /^\s*(?:$|[\w.%+-]+@[\w.-]+\.[a-z]{2,})\s*$/i
