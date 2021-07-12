//
//  ___FILENAME___
//  ___PROJECTNAME___
//
//  Created by ___FULLUSERNAME___ on ___DATE___.
//  Copyright (c) ___YEAR___ ___ORGANIZATIONNAME___. All rights reserved.
//
//  This file was generated by ListPage Templates
//

import UIKit

class  ___VARIABLE_moduleName___ListCell: MGSwipeTableCell {

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

    override func awakeFromNib() {
        super.awakeFromNib()
        setupUI()
    }

    private func setupUI() {
        selectionStyle = .none
        
        self.rightButtons = [rightButton]
        self.rightSwipeSettings.transition = .static
        self.rightSwipeSettings.topMargin = 9
        self.rightSwipeSettings.bottomMargin = 9
        self.delegate = self

        // 在这里写UI初始化相关逻辑
    }
}


// MARK: - Extensions -

extension ___VARIABLE_moduleName___ListCell: MGSwipeTableCellDelegate {
    func swipeTableCell(_ cell: MGSwipeTableCell, canSwipe direction: MGSwipeDirection, from point: CGPoint) -> Bool {
        if point.x < self.frame.width / 2.0 {
            return false;
        }
        return true
    }
}
