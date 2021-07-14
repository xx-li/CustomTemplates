PARENT_CLASS = "UITableViewCell"

PARENT_CLASS__EDIT = "MGSwipeTableCell"

CALL_SETUP_RIGHT_BUTTONS = "setupRightButtons()"

RIGHT_BUTTONS_CREATE_AND_USE = """
    // MARK: - 右边操作按钮 -

    private func setupRightButtons() {        
        self.rightButtons = [rightButton]
        self.rightSwipeSettings.transition = .static
        self.rightSwipeSettings.topMargin = 9
        self.rightSwipeSettings.bottomMargin = 9
        self.delegate = self
    }

    var didDeleteButtonClick: ((_ cell: ___VARIABLE_moduleName___ListCell) -> (Void))?
    
    lazy var rightButton:MGSwipeButton =  {
        let btn = MGSwipeButton.init(title: "删除", backgroundColor: UIColor.init(hex: "#FF6868"))
        btn.titleLabel?.numberOfLines = 0
        btn.titleLabel?.font = UIFont.dt_pingFangSC(withWeight: .medium, size: 14)
        btn.buttonWidth = 66.0
        btn.callback = { [weak self] (cell) -> (Bool) in
            if let didDeleteButtonClick = self?.didDeleteButtonClick {
                didDeleteButtonClick(self!)
            }
            return true
        }
        return btn
    }()
"""

RIGHT_BUTTONS_DELEGATE = """
// MARK: - Extensions -

extension ___VARIABLE_moduleName___ListCell: MGSwipeTableCellDelegate {
    func swipeTableCell(_ cell: MGSwipeTableCell, canSwipe direction: MGSwipeDirection, from point: CGPoint) -> Bool {
        if point.x < self.frame.width / 2.0 {
            return false;
        }
        return true
    }
}
"""

# ListCell和ListCell的xib都会调用，xib文件匹配不上字符，不会对内容做任何修改，非list页面输出为None，刚好满足需求。
def replace(str, type):
    res = str
    if "List" in type.value:
        if "Edit" in type.value:
            res = res.replace('%PARENT_CLASS%', PARENT_CLASS__EDIT)
            res = res.replace('%CALL_SETUP_RIGHT_BUTTONS%', CALL_SETUP_RIGHT_BUTTONS)
            res = res.replace('%RIGHT_BUTTONS_CREATE_AND_USE%', RIGHT_BUTTONS_CREATE_AND_USE)
            res = res.replace('%RIGHT_BUTTONS_DELEGATE%', RIGHT_BUTTONS_DELEGATE)
        else:
            res = res.replace('%PARENT_CLASS%', PARENT_CLASS)
            res = res.replace('%CALL_SETUP_RIGHT_BUTTONS%', "")
            res = res.replace('%RIGHT_BUTTONS_CREATE_AND_USE%', "")
            res = res.replace('%RIGHT_BUTTONS_DELEGATE%', "")
    else:
        res = None
    return res

def replaceXib(str, type):
    if "List" in type.value and "Xib" in type.value:
        return str
    else:
        return None