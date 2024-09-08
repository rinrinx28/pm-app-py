# / M4 start
def handler_data_m4(
    self,
    i,
    t,
    col_e_m3,
    notice_colorM4,
    value1_4,
    countRow,
    col_a,
    thong_range_1,
    stt_cot,
    col_d,
    col_t,
    col_e,
    col_e_m2,
    isEqual,
    total_column,
    isNoticeCount,
    col_color,
    col_color_m2,
    col_color_m3,
    isNoticeColor,
    isNoticeColor_m2,
    isNoticeColor_m3,
    item_date,
    col_e4,
    row_thong,
    isDeleted,
):
    math_count_handler_m4 = f"{col_e_m3}:{i}:_color_m4"
    if not math_count_handler_m4 in self.count_handler:
        self.count_handler[math_count_handler_m4] = 1
    else:
        self.count_handler[math_count_handler_m4] += 1

    # / End check col_stt table count
    stt_count_with_d_m4 = self.count_handler[
        math_count_handler_m4
    ]  # So thu tu cua so dem
    if stt_count_with_d_m4 <= 1:
        # / Start count color with col_e
        col_e_count_m4 = f"{col_e_m3}:{stt_count_with_d_m4}:col_e_m4"
        if not col_e_count_m4 in self.count_handler:
            self.count_handler[col_e_count_m4] = 1
        else:
            self.count_handler[col_e_count_m4] += 1
        col_e_m4 = self.count_handler[col_e_count_m4]  # so dem bang mau
        isNoticeColor_m4 = self.checkNotice(
            col_e_m4,
            notice_colorM4[0],
            notice_colorM4[1],
        )
        find_null_color_m4 = (1 if col_e_m3 - value1_4 > 0 else 0) * (
            col_e_m3 - value1_4
        )
        find_stt_color_m4 = stt_count_with_d_m4 - 1
        find_next_color_m4 = (col_e_m3 - value1_4) * 1
        col_color_m4 = (
            find_next_color_m4 + find_null_color_m4 + find_stt_color_m4
        )  # vi tri col cua item bang mau

        if isEqual:
            self.count_handler[col_e_count_m4] = 0
        # / Add data to table color 4
        dataColorM4 = {
            "row": countRow,
            "col": col_color_m4,
            "data": f"{col_a}/{t + thong_range_1 + 1}/{stt_cot}/{col_d} - {col_t}/{col_e}/{col_e_m2}/{col_e_m3}/{col_e_m4}",
            "color": isEqual,
            "action": {
                "name": "count",
                "row": countRow,
                "col": total_column,
                "isColor": isNoticeCount,
            },
            "actionM1": {
                "name": "color",
                "row": countRow,
                "col": col_color,
                "isColor": isNoticeColor,
            },
            "actionM2": {
                "name": "color",
                "row": countRow,
                "col": col_color_m2,
                "isColor": isNoticeColor_m2,
            },
            "actionM3": {
                "name": "color",
                "row": countRow,
                "col": col_color_m3,
                "isColor": isNoticeColor_m3,
            },
            "notice": isNoticeColor_m4,
            "date": item_date,
            "color_value": col_e4,
            "col_d": col_e_m3,
            "thong": {
                "row": row_thong,
                "col": t + 5,
                "col_a": (col_t if col_t != "?" else col_a),
                "isCol_a": (False if col_t != "?" else True),
            },
            "isDeleted": isDeleted,
        }
        return {"m4": dataColorM4, "object": {col_e_m4, isNoticeColor_m4, col_color_m4}}
